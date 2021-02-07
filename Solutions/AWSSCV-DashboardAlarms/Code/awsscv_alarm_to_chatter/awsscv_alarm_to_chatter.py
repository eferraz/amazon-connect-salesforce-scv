from awsscv.sf import Salesforce

logger = logging.getLogger()

def lambda_handler(event, context):
    sf = Salesforce()

    try:
        for record in event['Records']:
            results = sf.create_formatted_chatter_post('0F94W000000pThySAE', format_record(record), 'AllUsers');

        return { "Success": True, "Id": results['id'] }

    except Exception as err:
        return { "Success": False, "Error": str(err) }

def format_record(record):
    messageSegments = []

    messageSegments.extend([
        { 'markupType': 'Paragraph', 'type': 'MarkupBegin' },
        { 'markupType': 'Bold', 'type': 'MarkupBegin' },
        { 'text': record['Sns']['Subject'], 'type': 'Text'},
        { 'markupType': 'Bold', 'type': 'MarkupEnd' },
        { 'markupType': 'Paragraph', 'type': 'MarkupEnd' }
    ])

    message = json.loads(record['Sns']['Message'])

    trigger = message['Trigger']

    del message['Trigger']

    for key in message:
        value = message[key]

        print('Processing: {} - {}'.format(key, value))
        messageSegments.extend([
            { 'markupType': 'Paragraph', 'type': 'MarkupBegin' },
            { 'text': '{} - {}'.format(key, value), 'type': 'Text' },
            { 'markupType': 'Paragraph', 'type': 'MarkupEnd' }
        ])

    messageSegments.extend([
        { 'text': 'Trigger', 'type': 'Text'},
        { 'markupType': 'UnorderedList', 'type': 'MarkupBegin' }
    ])

    for key in trigger:
        value = trigger[key]

        messageSegments.extend([
            { 'markupType': 'ListItem', 'type': 'MarkupBegin' },
            { 'text': '{} - {}'.format(key, value), 'type': 'Text' },
            { 'markupType': 'ListItem', 'type': 'MarkupEnd' }
        ])


    messageSegments.extend([
        { 'markupType': 'UnorderedList', 'type': 'MarkupEnd' }
    ])

    return messageSegments
