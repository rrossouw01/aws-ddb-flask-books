import boto3

#def _get_default_session():
#    if DEFAULT_SESSION is None:
#        setup_default_session()
#    return DEFAULT_SESSION
#
#def setup_default_session(**kwargs):
#    DEFAULT_SESSION = Session(**kwargs)

#parser = argparse.ArgumentParser()
## other args...
#parser.add_argument('--profile')
#args = parser.parse_args()
#session = boto3.Session(profile_name=args.profile)

## https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html
session = boto3.Session(profile_name='default', region_name='us-east-1')
print(session.client('sts').get_caller_identity())

#sts = boto3.client('sts')
#print(sts.get_caller_identity())

#session = boto3.Session()
#s3 = session.client('s3')
ddb = session.resource('dynamodb')
#print(list(ddb.tables.all()))

def create_tables():
    table = ddb.create_table (
        TableName = 'Book1',
            KeySchema = [
              {
                "AttributeName": "id",
                "KeyType": "HASH"
              },
              {
                "AttributeName": "author_id",
                "KeyType": "RANGE"
              }
            ],
            AttributeDefinitions = [
              {
                "AttributeName": "author_id",
                "AttributeType": "S"
              },
              {
                "AttributeName": "id",
                "AttributeType": "S"
              }
            ],
            BillingMode = "PAY_PER_REQUEST"
    )
    print(table)

    table = ddb.create_table (
        TableName = 'Author1',
            KeySchema = [
              {
                "AttributeName": "author_id",
                "KeyType": "HASH"
              }
            ],
            AttributeDefinitions = [
              {
                "AttributeName": "author_id",
                "AttributeType": "S"
              }
            ],
            BillingMode = "PAY_PER_REQUEST"
    )
    print(table)

#table = dynamodb.Table('Employees')
#
#response = table.put_item(
#Item = { 
#     'Name': 'Kelvin Galabuzi',
#     'Email': 'kelvingalabuzi@handson.cloud'
#       }
#)
#print(response)
#

def load_data():
    table = ddb.Table('Author1')

    with table.batch_writer() as batch:
        batch.put_item(Item={"author_id": "0001", "author_name": "Riaan Rossouw"}),
        batch.put_item(Item={"author_id": "0002", "author_name": "Agatha Christie"})
    print(batch)

    table = ddb.Table('Book1')

    with table.batch_writer() as batch:
        batch.put_item(Item={"id": "0001", "author_id": "0001", "title": "Mysterious Affair at Styles"}),
        batch.put_item(Item={"id": "0002", "author_id": "0002", "title": "Cloud for Dummies"}),
        batch.put_item(Item={"id": "0003", "author_id": "0001", "title": "Mysterious Affair at Styles-2"}),
    print(batch)

#
#table = dynamodb.Table('Employees')
#
#response = table.scan()
#response['Items']
#
#print(response)
#
## boto3 ddb query
#response = table.query(KeyConditionExpression=Key('Name').eq('Luzze John'))
#
#print("The query returned the following items:")
#for item in response['Items']:
#    print(item)

#create_tables()
load_data()