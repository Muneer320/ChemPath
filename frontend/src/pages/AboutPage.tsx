import React from "react";
import { Alert, Container, Link, Paper, Typography } from "@mui/material";

const AboutPage: React.FC = () => (
  <Container maxWidth="md">
    <Typography variant="h4" component="h1" gutterBottom>About ChemPath</Typography>
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography paragraph>
        ChemPath is a learning archive from a chemistry pathway prototype. This version has a read-only local graph of 21 compounds and 23 reaction variants. It can show several loop-free routes and reagent alternatives where the small dataset permits them.
      </Typography>
      <Typography paragraph>
        Routes are ordered by a simple teaching-cost score in the data. That score is an educational display heuristic, not a prediction of yield, safety, laboratory feasibility, or the best synthesis. Formula strings are for display; each compound has a stable ID and searchable aliases.
      </Typography>
      <Typography>
        The subset is incomplete and has not been individually checked against a full curriculum. Use your textbook and instructor to verify reaction conditions. The original aim of a large NCERT/JEE/NEET database remains future work.
      </Typography>
    </Paper>
    <Alert severity="info" sx={{ mb: 3 }}>The app is an educational path explorer. It does not provide laboratory instructions or a verified synthesis plan.</Alert>
    <Typography variant="body2">
      For reference, see the official NCERT chapters on <Link href="https://ncert.nic.in/textbook/pdf/lech201.pdf" target="_blank" rel="noopener noreferrer">haloalkanes</Link> and the <Link href="https://ncert.nic.in/textbook.php?lech2=3-7" target="_blank" rel="noopener noreferrer">Chemistry II textbook</Link>.
    </Typography>
  </Container>
);

export default AboutPage;
