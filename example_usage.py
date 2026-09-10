from client import ReedSolomonCodec

def main():
    print("=== Testing Reed-Solomon Error Correction Codec ===")
    rs = ReedSolomonCodec(nsym=4)
    msg = [65, 66, 67, 68] # ASCII 'ABCD'
    codeword = rs.encode(msg)
    print("Encoded codeword:", codeword)
    assert len(codeword) == 8

    syndromes = rs.verify_syndromes(codeword)
    print("Verification syndromes (all zeros => clean):", syndromes)
    assert all(s == 0 for s in syndromes)
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
