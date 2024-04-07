# CloudSense Backend

### Tech Stack : 
- Django Rest framework
- 5 minute interval CRON job using django-cron and crontab
- Website status checks using python requests library
- OpenAI for recommendation

### How to Configure : 
Please setup a virtual environment prior to installing any dependencies

```bash
git clone https://github.com/AceHack-Brainstorm/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Optionally, for setting up CRON for a 5 minute status check, setup the following CRON tab entry using `crontab -e`
```sh
*/5 * * * *  source /home/monitor-backend/env/bin/activate && python3 /home/monintor-backend/backend/manage.py runcrons > /var/log/cronjob.log
```

# Working
### The services are setup as individual monitors
- As soon as a new service gets added, within the next 5 minutes it gets picked up by the CRON function and its respective status check logs are then populated in the mmonitoring_log database model.
- Each service has a detailed explanation about the architecture and tech stack, so that the system can understand and have a technical context before recommending a proper solution.
- The text in the architecture field is added as a system context in the OpenAI call.

[service.png]

### Monitor Logs
- Monitor logs have a foreign key relationship with the Service entity.
- Each log item is tied to a service and contains the datetime, HTTP status code and latency in milli-seconds.

[monitor_logs.png]
[monitor_log.png]

### Recommendation Engine
- If the service status code is 200, then a recommendation won't be provided, and a catch-all service is up message will be displayed instead.
- If the service is having a non 200 (OK) status, then the tech-stack's context as well as the current status code will be sent to OpenAI for a possible solution.

### Sample Prompt of the OpenAI Call
```yaml
- System : You are a helpful assistant designed to help system technicians in fixing the server issues.
- System : This is an Angular application deployed Deployed on AWS Cloudfront through an S3 bucket. While setting up, this application might return a 404 or 403 status code on some routes due to the way Angular behaves with static web servers. The sysadmin will need to configure the webserver such that any unmatched routes also gets routed to the index.html with a 200 status code
- User : I checked the system, but the HTTP status is 404. Can you tell the possible solution?
```

### Sample Response for the above prompts.

To resolve the issue of receiving a 403 status code on some routes in the Angular application deployed on AWS CloudFront through an S3 bucket, you need to ensure that the webserver is configured to route all unmatched routes to the index.html file with a 200 status code. This will allow the Angular application to handle the routing internally.\n\nHere's how you can configure this in an S3 bucket:\n\n1. **Navigate to the S3 Bucket**: Go to the AWS Management Console and open the S3 service.\n\n2. **Select S3 Bucket**: Click on the S3 bucket that is hosting your Angular application.\n\n3. **Enable Static Website Hosting**: If you haven't already, enable static website hosting for your S3 bucket. You can do this by going to the bucket properties, selecting \"Static website hosting,\" and setting the index document as index.html.\n\n4. **Edit Bucket Policy**: Edit the bucket policy to include rules that redirect requests to the `index.html` file. You can use the following bucket policy as an example:\n   ```json\n   {\n       \"Version\": \"2012-10-17\",\n       \"Statement\": [\n           {\n               \"Sid\": \"AngularRoutesRule\",\n               \"Effect\": \"Allow\",\n               \"Principal\": \"*\",\n               \"Action\": \"s3:GetObject\",\n               \"Resource\": \"arn:aws:s3:::YOUR_BUCKET_NAME/*\",\n               \"Condition\": {\n                   \"StringLike\": {\n                       \"s3:ExistingObjectTag/angular\": \"true\"\n                   }\n               },\n               \"ResponseContentDisposition\": \"inline\",\n               \"ResponseContentType\": \"text/html\",\n               \"ResponseMetadataDirective\": \"REPLACE\",\n               \"HttpErrorCodeReturnedEquals\": \"403\",\n               \"Redirect\": {\n                   \"HostName\": \"YOUR_BUCKET_NAME.s3-website-YOUR_REGION.amazonaws.com\",\n                   \"ReplaceKeyPrefixWith\": \"#/index.html\",\n                   \"Protocol\": \"https\"\n               }\n           }\n       ]\n   }\n   ```\n   Replace `YOUR_BUCKET_NAME` with your S3 bucket name and `YOUR_REGION` with your AWS region.\n\n5. **Add Metadata**: Update the metadata for the objects in your S3 bucket. Add the `angular` tag with a value of `true` to files that should be redirected to `index.html`.\n\n6. **Invalidate CloudFront Cache**: After making these changes, you may need to invalidate the CloudFront cache to ensure that the new configurations take effect.\n\nBy following these steps, you should be able to configure your S3 bucket to route all unmatched routes to the `index.html` file with a 200 status code, allowing your Angular application to handle the routing correctly.