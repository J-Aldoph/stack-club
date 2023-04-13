from aws_cdk import Stack, aws_ec2, aws_s3, aws_iam, Duration 

from constructs import Construct

class VpcAlphaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = aws_ec2.Vpc(self, "VpcAlpha", 
            cidr="10.42.0.0/16",
            subnet_configuration= [
                { 
                    "cidrMask": 24, 
                    "name": 'ingress', 
                    "subnetType": aws_ec2.SubnetType.PUBLIC
                },{ 
                    'cidrMask': 24, 
                    "name": 'application', 
                    'subnetType': aws_ec2.SubnetType.PRIVATE_WITH_EGRESS 
                }, { 
                    'cidrMask': 28, 
                    'name': 'rds', 
                    'subnetType': aws_ec2.SubnetType.PRIVATE_ISOLATED
                } 
            ]
        )
        s3LogBucket = aws_s3.Bucket(self, "LogBucket", 
            block_public_access = aws_s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl = True,
            versioned= True,
            access_control= aws_s3.BucketAccessControl.LOG_DELIVERY_WRITE,
            encryption= aws_s3.BucketEncryption.S3_MANAGED
        )
        vpcFlowLogRole = aws_iam.Role(self, "vpcFlowLogRole", assumed_by= aws_iam.ServicePrincipal("vpc-flow-logs.amazonaws.com"))

        s3LogBucket.grant_write(vpcFlowLogRole, "sboxVpcFlowLogs/*")

        aws_ec2.FlowLog(self, 'sboxVpcFlowLogs', 
            destination= aws_ec2.FlowLogDestination.to_s3(s3LogBucket,"sboxVpcFlowLogs/*"),
            traffic_type = aws_ec2.FlowLogTrafficType.ALL,
            flow_log_name = "sharedVpcFlowLogs", 
            resource_type= aws_ec2.FlowLogResourceType.from_vpc(vpc)
        )

        vpc.add_gateway_endpoint("s3Endpoint",
            service= aws_ec2.GatewayVpcEndpointAwsService.S3    
        )

        allOutboundSG = aws_ec2.SecurityGroup(self, "allOutboundSG",
            vpc=vpc,
            allow_all_outbound= True
        )
    
        allOutboundSG.add_ingress_rule(aws_ec2.Peer.ipv4(vpc.vpc_cidr_block), aws_ec2.Port.tcp(443), 'HTTPS Ingress')
        allOutboundSG.add_ingress_rule(aws_ec2.Peer.ipv4(vpc.vpc_cidr_block), aws_ec2.Port.tcp(22), 'SSH Ingress')

