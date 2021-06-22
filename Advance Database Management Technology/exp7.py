num_sites = int(input("Enter the total number of sites: "))
res_site = int(input("Enter the result site number: "))
site_size = [None] * num_sites
transfer_size = [None] * num_sites

# Accept data information for each site(check for availability)

for i in range(0, num_sites):
    is_available = input(
        "Is data for site {} available? press y or n: ".format(i + 1))

    if (is_available == 'y'):
        num_tuples = int(input("Enter number of tuples: "))
        size = int(input("Enter size of each tuple: "))

        site_size[i] = num_tuples * size

    else:
        site_size[i] = 0

# Accept result relation data

print("\nResult relation data input: ")
num_tuples = int(input("Enter number of tuples: "))
size = int(input("Enter size of each tuple: "))
res_data = num_tuples * size

print()

(strategy, total_data, total_data_transfer) = (0, 0, 0)

# Find total strategies and calculate data transfer for each strategy

for i in range(0, num_sites):
    total_data = 0
    if (i == res_site - 1):
        for j in range(0, num_sites):
            if (j != res_site - 1):
                total_data += site_size[j]
        strategy += 1
        print("Strategy Id:", strategy)
        print("Total Data Transfer:", total_data_transfer, "\n")

        transfer_size[i] = total_data
    else:
        for k in range(0, num_sites):
            if (k != i):
                print("Transfer data from site ", k, " to site ", i)
                total_data += site_size[k]

        total_data_transfer = total_data + res_data
        strategy += 1
        transfer_size[i] = total_data_transfer
        print("Strategy Id:", strategy)
        print("Total Data Transfer:", total_data_transfer, "\n")

print("\n")

print("Best Transfer size: ", min(transfer_size))
print("Best strategy ID: ", transfer_size.index(min(transfer_size))+1)
