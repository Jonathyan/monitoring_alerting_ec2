aws cloudformation deploy \
    --template-file CreateSnsTopics.yaml \
    --stack-name mcs-sns-topics \
    --region eu-central-1 \
    --profile AWS_CLI_PROFILE_YOU_USE \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM \
    --parameter-overrides \
PublishScope="WHOLE_ORGANIZATION_OR_NOT" \
OrgId="ORGANIZATIONS_ID" \
AlertPrefix="NAME_OF_ALERT_TOPIC"