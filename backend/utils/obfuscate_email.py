def obfuscated_email(email: str, obfuscated_length: int) -> str:
    # how many visible characters do we want to keep?
    # luis.martinez@gmail.com -> lu**********@gmail.com
    characters = email[:obfuscated_length]

    # split the email into two parts, the username and the domain
    # luis.martinez@gmail.com -> luis.martinez, gmail.com
    first, last = email.split("@")

    # obfuscate the username
    return characters + ("*" * len((first) - obfuscated_email)) + "@" + last
