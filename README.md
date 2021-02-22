# A serverless architecture to manage servers

A solution that shows what a cloud native monitoring and alerting solution for servers on a single cloud (AWS) looks like using “built-in” serverless cloud services. To keep it simple and help you understand the idea, we’re only looking at EC2 metrics. The goal here is to minimize time and resources spent on configuration and maintenance, minimize service costs, focus on the ability to use it on a large-scale environment and to get started quickly for new environments that need to be managed. So, to minimize tinkering and to maximize value.

The architecture consists of three parts: 
1.	Creating a place to receive and pass on notifications;
2.	Figuring out what needs to be measured and finally;
3.	Creating alerts to send actionable notifications. 


# Plain and simple EC2 instances to explain the solution

## Requirements
Before we start, there are some requirements. 
- EC2 servers are properly managed
- Systems Manager (SSM) installed
- CloudWatch Agents installed
- Memory and disk space utilization metrics are being sent to CloudWatch Alarms.
- AWS CLI locally installed
- AWS SAM CLI locallly installed
- AWS Config configured

![Alt text](./architecture.png?raw=true "Solution Architecture")

## SNS - Notifications
For the first part, we prepare AWS SNS to receive notifications about the EC2 instances and pass them on via mail, Slack or something else of your liking. In this demo you see my mail address in the screenshot below. To deploy SNS we use a separate CloudFormation stack to have flexibility in your communications to the engineering team.
 
- Open "TestCfSns.sh"
- Fill in the parameters PublishScope, OrgId and/or AlertPrefix. Not required, if empty use: ""
- To access the right AWS account, fill in your AWS profile as you have defined it in ~/.aws/config.
- Launch the CloudFormation template by running the script you just filled in. Go to directory of the file and execute: ./TestCfSns.sh

## Config (Advanced Queries) - Know what needs to be measured
In the second part, we need to know what needs to be measured. In this example we query our cloud environment what EC2 instances are running with Advanced Queries within AWS Config. Queries can get expensive if you are checking every minute, so we settle for a daily scan. According to the running EC2 instances found, we kick-off a CloudFormation stack. In the picture below we find two instances. This first part is automated with Python (boto3) in a Lambda function deployed with AWS SAM. So we can set it and forget it.

- Look up the ARN of the SNS ls in the Management Console, go directly to SNS (or find it via CloudFormation --> Resources --> SNS).
- Install and run docker on your MacBook/Windows
- Go to the SAM directory: cd sam-monitoring
- Let SAM make a build: sam build --use-container
- Deploy with SAM by following the wizard in the cli: sam deploy --guided --profile INSERT_YOUR_PROFILE_NAME_HERE

 
## CloudFormation & CloudWatch Alarms - only use alarms that you need
Finally, in the third part the CloudFormation stack is being created to manage our Alarms that send actionable notifications. With this stack CloudWatch Alarms are being created and gracefully deleted according to the scheduled findings of Config, so you don’t end up with an expensive mess when instances are terminated. 

# The Conclusion

Within this solution, we have seen we only have (1) a CloudFormation stack to launch for setting up SNS, and (2) a Lambda function to deploy to start searching and setting up things to measure. When you extend it to other metrics, you can easily manage a large-scale environment cost effectively and quickly set up monitoring & alerting using infrastructure as code.
