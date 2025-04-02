# vectorauth

Vectorauth has designed, implemented and verified a novel cyber authentication method that uses Ultra-Wide-Band(UWB) wireless technology and Voice-ID and speech recognition AI models to make the cyber authentication secure, fast and automatic. VectorAuth accurately detects the user’s position to predict if the user needs to sign in. When confirmed, users use their voice to sign in without having to enter any passwords, and the access will automatically be revoked as soon as users move away from the device to avoid any security breaches. We built a prototype to demonstrate the complete authentication flow. The results showed that VectorAuth is a promising new authentication method. 

## The origin of our project idea

* One day in a hospital, we noticed that doctors still need to use their badges or enter a password to either enter a gate or access files on a PC, even during emergency.
* Traditional authentication methods, such as passwords and two-factor authentication (2FA), have several major shortcomings:
  * Passwords can easily be stolen
  * That verification SMS may take a long time to arrive
  * The security key usually grant 24 hour access which can cause security breach

## Our research goal
* Design, implement and verify a novel authentication solution that are:
  * Accurate -> Detects the user’s position in centimeter accuracy to predict if the user needs to sign in. 
  * Fast -> Use user’s voice to sign in with a secret phrase in seconds 
  * Secure -> Access will automatically be revoked as soon as users move away



## Our Innovative Authentication Flow
* Accurately detects the user’s position to predict if the user needs to sign in. 
* Users use their voice to sign in without having to enter any passwords.
* The access will automatically be revoked as soon as users move away from the device to avoid any security breaches.
* User set its secret phrase for even higher security
<img width="483" alt="Screen Shot 2025-04-01 at 7 52 34 PM" src="https://github.com/user-attachments/assets/8d0ed379-b672-464e-94dc-e623739c04ac" />


## Our Innovative Hardware Design
* Use 5 Qorvo DWM1001 development boards for our prototype. 
* 1 is configured as a tag, or the authentication token that a user carries
* 3  are configured as anchors and 1 is configured as a listener. They are fixed in position and connected to the laptop through a USB port. Together, they detect tag’s position with high accuracy (<50 cm error) and low latency (<2 seconds)
<img width="890" alt="Screen Shot 2025-04-01 at 7 48 55 PM" src="https://github.com/user-attachments/assets/82703dec-123f-47f7-a144-c12fb5e34417" />

## Python Code
* Multiple Python programs are written to implement the authentication flow. They are all uploaded to Github.
* demo.py describe and demo the end-to-end flow
* record.py is how to record user's voice to creat an identity for each user
* verify.py is how user's voice is authenticated

## Contact us
For more information, please go to [VectorAuth.net](https://vectorauth.net)
