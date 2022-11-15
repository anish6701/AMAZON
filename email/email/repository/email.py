#Below importing required dependencies...
import boto3,math,random,datetime
from fastapi import HTTPException
from starlette import status
import schemas
from database import engine
from botocore.exceptions import ClientError

SENDER = " SENDER_NAME <SENDER_EMAIL>"
RECIPIENT = " RECIPIENT_NAME <RECIPIENT_EMAIL>"
digits = '0123456789'
Otp = ''
for i in range(6):
    Otp += digits[math.floor(random.random() * 10)]
    otp = Otp
    msg = otp
def mail():
  # CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "YOUR_REGION_NAME"
    SUBJECT = "Email verification" #SUBJECT FOR YOUR EMAIL

    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
             )

    #BELOW IS HTML BODY TEXT and THIS IS FOR EXAMPLE OF TESTING EMAIL WHICH YOU CAN USE.
    BODY_HTML = f"""<html>
    <body>
    <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
    <div style="margin:50px auto;width:70%;padding:20px 0">
    <div style="border-bottom:1px solid #eee">
      <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">
          <img src="YOUR_ORGANIZATION_IMAGE_SOURCE" alt="">
      </a>
    </div>
    <p style="font-size:1.1em">Hi, {RECIPIENT}</p>
    <p>Thank you for choosing. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
    <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
    <p style="font-size:0.9em;">Regards,<br/> YOUR_NAME </p> # add changes to yours tag
    <hr style="border:none;border-top:1px solid #eee" />
    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
    <p>This message was sent from a notification-only email address that does not accept incoming email. Please do not reply directly to this message. YOUR_NAME.</p>
    </div>
    </div>
    </div>
    </body>
    </html>"""

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', aws_access_key_id='YOUR_AWS_KEY_ID',
                        aws_secret_access_key='YOUR_AWS_ACCESS_KEY',
                        region_name= AWS_REGION) #defined above

    #Try to send the email.
    try:
        #Provide the contents of the email.

        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        response = {"status": False, "message": e.response['Error']['Message'],
                    "message_id": "undefined",
                    "response": e.response}
        print("Response Key:", response.keys())
        print(response)

        return response
    else:
        response = {"status": True,
                    "message": "Email Successfully Sent.",
                    "OTP":otp}

        test = engine.execute("insert into email (email,otp,created_at) values('"+str(RECIPIENT)+"', '"+str(otp)+"','"+str(datetime.datetime.now())+"')")

        return response

#BELOW FUNTCTION TO VERIFY THE RECIEVED OTP.
def verify(request:schemas.Eml):
    entered_otp = request.otp
    otpsql = engine.execute('select user_id,otp from email order by user_id desc')

    data = otpsql.fetchone()

    print('data', data['user_id'])
    print('data', data['otp'])

    saved_otp = data['otp']
    user_id = data['user_id']
    
    if entered_otp == int(saved_otp):
        print('in if')

        status_update =engine.execute("update email set status=1 where user_id='"+str(user_id)+"'")
        msg = {"status": "success",
               "Email": f'{RECIPIENT}',
               "OTP": f'{otp}',
               "detail": f'Email Verified'}
        return msg
    else:
        print('in else')
        msg = {"status": "failed",
               "detail": f'Entered OTP : {otp} does not match'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=msg)


