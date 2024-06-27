#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import boto3

def modify_instance_metadata(instance_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.modify_instance_metadata_options(
        InstanceId=instance_id,
        HttpTokens='required',
        HttpEndpoint='enabled'
    )
    return response

def run_module():
    module_args = dict(
        instance_id=dict(type='str', required=True),
        region=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        response=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    instance_id = module.params['instance_id']
    region = module.params['region']

    try:
        response = modify_instance_metadata(instance_id, region)
        result['changed'] = True
        result['response'] = response
    except Exception as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
