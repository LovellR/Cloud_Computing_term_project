from instance_operations import (
    init as init_ec2,
    instance_operations_menu
)

from SSM_operations import (
    init_ssm, 
    SSM_operations_menu
)

from Storage_operations import (
    storage_operations_menu
)

from Network_operations import (
    network_operations_menu
)

from AMI_operations import (
    AMI_operations_menu
)

if __name__ == "__main__":
    ec2 = init_ec2()
    ssm = init_ssm()

    while True:
        print("\n------------------------------------------------------------")
        print("                 Amazon AWS Control Panel                   ")
        print("------------------------------------------------------------")
        print("  1. instance operations          2. SSM operations         ")
        print("  3. AMI operations               4. storage operations     ")
        print("  5. network operations                                     ")
        print("                                 99. quit                   ")
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
            instance_operations_menu(ec2)
        elif number == 2:
            SSM_operations_menu(ec2, ssm)
        elif number == 3:
            AMI_operations_menu(ec2)
        elif number == 4:
            storage_operations_menu(ec2)
        elif number == 5:
            network_operations_menu(ec2)
        else:
            print("Invalid option!")