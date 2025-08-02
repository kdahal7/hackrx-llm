const express = require('express');
const app = express();
const port = process.env.PORT || 4000;

app.use(express.json());

app.post('/api/v1/hackrx/run', (req, res) => {
  const query = req.body.query;

  // Mock response for testing
  res.json({
    decision: "Approved",
    amount: "₹10000",
    justification: "Yes, knee surgery is covered under the policy."
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
