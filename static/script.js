function runFunction() {
    const age = document.getElementById('age').value;
    const job = document.getElementById('job').value;
    const marital = document.getElementById('marital').value;
    const education = document.getElementById('education').value;
    const balance = document.getElementById('balance').value;
    const housing = document.getElementById('housing').value;
    const loan = document.getElementById('loan').value;
    const contact = document.getElementById('contact').value;
    const day = document.getElementById('day').value;
    const month = document.getElementById('month').value;
    const duration = document.getElementById('duration').value;

    fetch('/run_function', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            age: age,
            job: job,
            marital: marital,
            education: education,
            balance: balance,
            housing: housing,
            loan: loan,
            contact: contact,
            day: day,
            month: month,
            duration: duration
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Result: ${data.result}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
