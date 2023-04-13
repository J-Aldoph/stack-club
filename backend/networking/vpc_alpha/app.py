#!/usr/bin/env python3
import os

import aws_cdk as cdk

from vpc_alpha.vpc_alpha_stack import VpcAlphaStack


app = cdk.App()
VpcAlphaStack(app, "VpcAlphaStack"
    )

app.synth()
