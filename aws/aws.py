from instance_operations import (
    init as init_ec2,
    list_instances,
    available_zones,
    start_instance,
    stop_instance,
    create_instance,
    reboot_instance,
)
from SSM_operations import init_ssm, execute_condor_status

if __name__ == "__main__":
    ec2 = init_ec2()
    ssm = init_ssm()

    while True:
        print("\n------------------------------------------------------------")
        print("                 Amazon AWS Control Panel                   ")
        print("------------------------------------------------------------")
        print("  1. list instance                2. available zones        ")
        print("  3. start instance               4. available regions      ")
        print("  5. stop instance                6. create instance        ")
        print("  7. reboot instance              8. list images            ")
        print("  9. condor_status               99. quit                   ")
        print("------------------------------------------------------------")

        try:
            number = int(input("Enter an integer: "))
        except ValueError:
            print("Invalid input!")
            continue

        if number == 99:
            print("bye!")
            break
        elif number == 1:
            list_instances(ec2)
        elif number == 2:
            available_zones(ec2)
        elif number == 3:
            instance_id = input("Enter instance id: ").strip()
            if instance_id:
                start_instance(ec2, instance_id)
        elif number == 5:
            instance_id = input("Enter instance id: ").strip()
            if instance_id:
                stop_instance(ec2, instance_id)
        elif number == 6:
            ami_id = input("Enter AMI id: ").strip()
            if ami_id:
                create_instance(ec2, ami_id)
        elif number == 7:
            instance_id = input("Enter instance id: ").strip()
            if instance_id:
                reboot_instance(ec2, instance_id)
        elif number == 9:
            instance_id = input("Enter instance ID: ").strip()
            if instance_id:
                execute_condor_status(ssm, instance_id)
        else:
            print("Invalid option!")
