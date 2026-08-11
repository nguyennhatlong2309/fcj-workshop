---
title : "Resource Cleanup"
date : 2024-01-01 
weight : 6
chapter : false
pre : " <b> 5.6. </b> "
---

After completing the hands-on lab or when your internship ends, it is highly critical to clean up and delete all provisioned AWS resources to avoid unexpected charges (especially when your account exceeds the 12-month Free Tier limit).

---

#### Step-by-Step Resource Cleanup Guide:

##### Step 1: Terminate the EC2 Instance
1. Log in to the AWS Management Console and switch to the **Sydney region (`ap-southeast-2`)**.
2. Navigate to the **EC2 Console** -> Select **Instances** -> Find your `cafe-app-server` instance.
3. Check the instance -> Click **Instance state** -> Select **Terminate instance** (permanently deletes the virtual machine).
4. Click **Terminate** to confirm. Once terminated, all local Docker containers and volumes will be permanently deleted.

##### Step 2: Release the Elastic IP (Static IP)
*Note:* AWS charges a small fee for Elastic IP addresses that are allocated to your account but are not associated with any active EC2 instances.
1. In the EC2 Console, select **Elastic IPs** from the left menu.
2. Select the static IP address that was previously associated with the application server.
3. Click the **Actions** button at the top -> Select **Release Elastic IP addresses**.
4. Confirm by clicking **Release** to return the IP address to the AWS pool.

##### Step 3: Delete the Amazon S3 Bucket (`jenkam-images`)
AWS does not allow you to delete an S3 bucket that still contains objects. Therefore, you must empty it first:
1. Navigate to the **S3 Console** -> Click on your bucket **`jenkam-images`** (or the bucket name you created).
2. Click the **Empty** button in the top menu.
3. Type `permanently delete` in the confirmation box to delete all images in the `invoices/` and `temp/` directories -> Click **Empty**.
4. Return to the main S3 Buckets page -> Select the bucket -> Click the **Delete** button.
5. Enter the exact name of the bucket to confirm and click **Delete bucket** to permanently remove it.

##### Step 4: Delete the IAM Role and Security Group
1. **Delete IAM Role:** 
   * Navigate to the **IAM Console** -> Select **Roles** on the left menu.
   * Search for and select the **`Jenkam-EC2-Role`** role -> Click **Delete**.
   * Enter the role name to confirm deletion.
2. **Delete Security Group:**
   * Navigate to the **EC2 Console** -> Select **Security Groups** on the left menu.
   * Select the **`web-app-sg`** security group -> Click **Actions** -> Select **Delete security group**.
   * Confirm the deletion.

##### Step 5: Delete the CloudWatch Log Group and SNS Topic
1. **Delete Log Group:** 
   * Navigate to the **CloudWatch Console** -> Select **Log groups** -> Check the box for **`cfe-di-rom-logs`**.
   * Click **Actions** -> Select **Delete log group(s)** and confirm.
2. **Delete SNS Topic:**
   * Navigate to the **SNS Console** -> Select **Topics** -> Select the **`cfe-di-rom-alerts`** topic.
   * Click **Delete** and enter the confirmation phrase to delete it permanently (associated email subscriptions will be canceled automatically).