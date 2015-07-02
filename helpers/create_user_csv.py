from faker import Faker

def decide_role(n, roles):
    if((n+1) % 2 == 0):
        return roles[1]
    else:
        return roles[0]

def create_csv_file(path, number_of_users):
    f = Faker()
    roles = ['ordinary user', 'admin user']
    default_password = "secretPassword"
    with open(path, "w") as file_handle:
        file_handle.write("First Name,Last Name,Username,Email Address,Role,Password\n")
        for n in range(number_of_users):
            role = decide_role(n, roles)
            password = default_password
            file_handle.write("%s,%s,%s,%s,%s,%s\n" % (f.first_name(), f.last_name(), f.username(), f.email(), role, password))

if __name__ == "__main__":
    create_csv_file("users.csv", 3)
