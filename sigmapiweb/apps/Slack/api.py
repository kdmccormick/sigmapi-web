"""
API Endpoints for Slack Apps
"""
import json
import re

from django.http import JsonResponse, HttpResponse

from .utils import verify_sigma_poll_sig


def make_poll_usage_error(message, user_text):
    """
    Helper for creating the usage text response for Sigma Polls
    :param user_text: The command the user attempted to use
    """
    response = {
        "response_type": "ephemeral",
        "text": message + "\n"
                          "To create a poll, you need to format your query in the following way:\n"
                          "/sigmapoll \"Is this a poll?\" \"Yes\" \"No\"\n"
                          "This will create a poll with the question \"Is this a poll?\", and with the two possible "
                          "responses \"Yes\" and \"No\".\n"
                          "You invoked the following slash command: " + str(user_text)
    }
    return JsonResponse(response)


EMOJI_NUMS = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']


@verify_sigma_poll_sig
def sigma_poll_create(request):
    """
    Creates a poll from a slash command POST that slack will send us
    Format: "What should we eat today?" "Apples" "Oranges"
    """

    response_url = request.POST.get('response_url')
    original_text = request.POST.get('text')

    if original_text is None or response_url is None:
        return HttpResponse('POST missing required fields', status=400)

    # Split the text on any type of quote, and make sure there are at least two options
    args = re.split('["“”]', original_text)
    if len(args) < 7 or args[0] != '' or len(args) % 2 == 0 or args[1].strip() == "" or args[2] != " ":
        return make_poll_usage_error("Error: Invalid Message Format", original_text)

    poll_question = args[1]
    poll_options = []
    poll_buttons = []
    i = 3
    while i < len(args):
        if args[i].strip() == "" or args[i + 1].strip() != "":
            return make_poll_usage_error("Error: Invalid Message Format", original_text)
        poll_options.append(args[i].strip())

        index = len(poll_buttons)
        if index >= len(EMOJI_NUMS):
            return make_poll_usage_error("Error: Too many options provided (max is 9)", original_text)
        poll_buttons.append({
            "name": str(index),
            "text": EMOJI_NUMS[index],
            "type": "button",
            "value": str(index)
        })

        # Add 2 since the next element is a space
        i += 2

    poll_buttons.append({
        "name": "delete",
        "text": "Delete Poll",
        "style": "danger",
        "type": "button",
        "value": "delete",
        "confirm": {
            "title": "Delete Poll?",
            "text": "Are you sure you want to delete the poll?",
            "ok_text": "Yes",
            "dismiss_text": "No"
        }
    })

    poll_text = "*" + poll_question + "*\n"
    option_index = 0
    while option_index < len(poll_options):
        poll_text += EMOJI_NUMS[option_index] + " " + poll_options[option_index] + "\n\n"

        option_index += 1

    response = {
        "response_type": "in_channel",
        "replace_original": True,
        "delete_original": True,
        "text": poll_text,
        "attachments": [{
            "fallback": "You are unable to complete this survey",
            "color": "#4196ca",
            "callback_id": "poll_buttons",
            "actions": poll_buttons[0:5]
        }]
    }

    if len(poll_buttons) > 5:
        response['attachments'].append({
            "fallback": "You are unable to complete this survey",
            "color": "#4196ca",
            "callback_id": "poll_buttons",
            "actions": poll_buttons[5:]
        })

    return JsonResponse(response)


def format_user(user_id):
    """
    Formats a user id so it appears as @user in the slack
    """
    return "<@" + user_id + ">"


def process_sigma_poll_action(user_id, action, response):
    """
    Applies an action to a poll
    :param user_id: The ID of the user who did this action
    :param action: The action to perform
    :param response: The response object to modify
    :return: True if the message isn't being deleted
    """
    option_value = action['value']
    if option_value == 'delete':
        response.clear()
        response['delete_original'] = True
        return False

    option_value = int(option_value)

    poll_split = response['text'].split('\n')

    option_text_index = 2 * option_value + 1
    option_users_index = option_text_index + 1

    option_text_split = list(filter(None, re.split(" ", poll_split[option_text_index])))
    option_users = list(filter(None, poll_split[option_users_index].split(', ')))

    if format_user(user_id) in option_users:
        option_users.remove(format_user(user_id))
    else:
        option_users.append(format_user(user_id))

    # Update the users list
    poll_split[option_users_index] = ', '.join(str(x) for x in option_users)

    num_votes = len(option_users)

    poll_split[option_text_index] = option_text_split[0] + ' ' + option_text_split[1]
    if num_votes > 0:
        poll_split[option_text_index] += '    `' + str(num_votes) + "`"

    response['text'] = '\n'.join(str(x) for x in poll_split)

    return True


@verify_sigma_poll_sig
def sigma_poll_update(request):
    """
    Updates a Sigma Poll. This will either be a vote being cast, removed, or the creator
    requesting it to be deleted
    :param request:
    :return:
    """
    body = json.loads(request.POST.get('payload'))
    user = body['user']['id']

    response = {
        "replace_original": True,
        "text": body['original_message']['text'],
        "attachments": body['original_message']['attachments']
    }

    for action in body['actions']:
        if not process_sigma_poll_action(user, action, response):
            break

    return JsonResponse(response)
