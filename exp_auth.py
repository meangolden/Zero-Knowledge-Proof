"""
Created on Wed Mar 22 23:47:55 2023

This code is the outline of a zero-knowledge proof protocol for authentication.
The protocol is a modified code of the Chaum-Pederson
(https://www.cs.umd.edu/~waa/414-F11/IntroToCrypto.pdf page 377,subsection "3.2.
whereby the prover demonstrates knowledge of the private key corresponding to
the claimed identity through a series of computations mod p. The code runs on
an example case of a genuine prover for demonstration purposes.

@author: chrys_pas
"""
import random
import domain_parameters as dp

# initialise a dictionary for storing usernames and public keys
user_dict = {}


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Domain:
    """ A class that contains all constants"""
    q, p = 7433, 14867  # safe primes
    g, h = dp.find_primitives(q, p)  # fine elements of prime order q

    # Uncomment line below for a large-primes example
    # q, p, g, h = dp.read_large_domain()

    print(f"Agreed primes:")
    print(f"q = {q}")
    print(f"p = {p}")
    print(f"Agreed primitives of prime order q:")
    print(f"g = {g}")
    print(f"h = {h}\n")
    print()


def register(name, x=random.randint(2, Domain.p - 2)):
    assert isinstance(name, str), "name must be a string"
    assert isinstance(x, int) and 1 < x < Domain.p - 1, \
        "key must be an integer in the range [2, p-2]"

    print(f'Private key created:')
    print(f'x = {x}')
    print()

    # compute public key (y1, y2)
    y1 = pow(Domain.g, x, Domain.p)
    y2 = pow(Domain.h, x, Domain.p)

    # create an entry in the dictionary
    user_dict[name] = (y1, y2)
    print(f'Dictionary entry created:')
    print(f'User: {name}')
    print(f'Public Key: {(y1, y2)}')
    print()


def challenge(c=random.randint(2, Domain.p - 2)):
    """
        This function generates a challenge value.

        Args:
            c (int, optional): The challenge value to be set by the verifier. Defaults to a
                random integer within the range [2, p-2] (inclusive).

        Returns:
            int: The challenge value set by the verifier.
        Raises:

            AssertionError: If the input challenge value is not an integer or is not within
                the range [2, p-2].
        """
    assert isinstance(c, int) and 1 < c < Domain.p - 1, \
        "challenge must be an integer in the range [2, p-2]"
    print("Challenge set by the verifier:")
    print(f"c = {c}")
    print()
    return c


def proof(x, c, k=random.randint(2, Domain.p - 2)):
    """
        This function generates a zero-knowledge proof for the prover's knowledge of
        the private key x, given the challenge value c set by the verifier.

        Args:
            x (int): The prover's private key.
            c (int): The challenge value set by the verifier.
            k (int): A random integer generated by the prover as the private session key.
                     Default is a random integer within the range [2, p-2].

        Returns:
            tuple of three ints: (r1, r2, s), where r1 and r2 are integers that serve as a
            commitment to the public session key, and s is the prover's response value.
        """
    assert isinstance(x, int) and 1 < k < Domain.p - 1, \
        "private key must be an integer in the range [2, p-2]"
    assert isinstance(k, int) and 1 < k < Domain.p - 1, \
        "session key must be an integer in the range [2, p-2]"

    # Prover generates a commitment based on the private session key k.
    (r1, r2) = pow(Domain.g, k, Domain.p), pow(Domain.h, k, Domain.p)
    assert r1 != Domain.g and r2 != Domain.h, "Repeat the signing process by \
    choosing a different private session key (k)"
    print("Prover's commit values:")
    print(f"r1 = {r1}")
    print(f"r2 = {r2}")
    print()

    # Prover computes the response value
    s = k - c * x
    s = s % Domain.q
    print("Prover's response value:")
    print(f"s = {s}")
    print()
    return r1, r2, s


def verify(name, r1, r2, s, c):
    """
        Summary:
        This function performs a verification test on a given set of inputs to
        determine whether the proof provided by the prover is valid.

        Inputs:
            name: prover's name (str)
            r1, r2 : prover's commitment values (int)
            s: prover's response value (int)
            c: verifier's challenge (int)
        Outputs:
            Boolean - 'True' if verification is successful, 'False' otherwise
        """
    assert isinstance(name, str)
    # Verifier retrieves the public key
    y1, y2 = user_dict[name]

    # Verifier perfomrs a verification test
    v1 = pow(Domain.g, s, Domain.p) * pow(y1, c, Domain.p)
    v2 = pow(Domain.h, s, Domain.p) * pow(y2, c, Domain.p)
    v1 = v1 % Domain.p  # reduce mod p
    v2 = v2 % Domain.p
    print("Verification computed values:")
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")

    return v1 == r1 and v2 == r2


def main():

    dp.check_parameters(Domain.q, Domain.p, Domain.g, Domain.h)

    # Get prover's private key
    x = 342
    # Get prover's session private key (commitment nonce)
    # k = 3   # prover's session key

    # Get user's name and private key
    name = "Prutence"
    x = random.randint(2, Domain.p-2)

    # Register user with name and private key
    register(name, x)

    # Get the challenge
    c = challenge()

    # Generate proof of identity
    r1, r2, s = proof(x, c)

    # Verify proof of identity
    v = verify(name, r1, r2, s, c)

    if v:
        print("Successfull verification!")
    else:
        print('Access Denied')

if __name__ == "__main__":
    main()