# e-VoteSecure
Implementation of a Secure e-Voting system

# Usage
- Clone the repository
- Install streamlit using the following command
```bash
pip install streamlit
```

- Run the Trusted Authority server using the following command from the src directory
```bash
export FLASK_APP=trustedAuthority/app.py
python -m flask run
```

- To run the streamlit app, run the following command from the src directory
```bash
python -m streamlit run client/app.py
```

# TODO
- [x] Implement the universal verifiable e-voting system (global counter)
- [x] Implement the backend to simulate trusted authority for blindly signing the votes
- [x] Implement OTP based authentication for voters for voter registration
- [ ] Identify vulnerabilities and fix them
- [ ] Identify performance bottlenecks and fix them
- [ ] Remove Debug errors and warnings
- [ ] Add receipt