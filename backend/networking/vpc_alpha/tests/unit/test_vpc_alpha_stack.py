import aws_cdk as core
import aws_cdk.assertions as assertions

from vpc_alpha.vpc_alpha_stack import VpcAlphaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in vpc_alpha/vpc_alpha_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = VpcAlphaStack(app, "vpc-alpha")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
