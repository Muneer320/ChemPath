import React from "react";
import { Box, Button, Container, Typography, useTheme } from "@mui/material";
import { Link } from "react-router-dom";
import { SentimentVeryDissatisfied as SadIcon } from "@mui/icons-material";

const NotFoundPage: React.FC = () => {
  const theme = useTheme();

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "70vh",
          textAlign: "center",
          py: 8,
        }}
      >
        <SadIcon
          sx={{ fontSize: 80, color: theme.palette.primary.main, mb: 2 }}
        />

        <Typography variant="h2" component="h1" gutterBottom>
          404
        </Typography>

        <Typography variant="h4" gutterBottom>
          Page Not Found
        </Typography>

        <Typography
          variant="body1"
          color="textSecondary"
          paragraph
          sx={{ maxWidth: 500, mb: 4 }}
        >
          Oops! The page you're looking for seems to have reacted with something
          else and disappeared. Maybe it underwent a chemical transformation?
        </Typography>

        <Box sx={{ display: "flex", gap: 2 }}>
          <Button
            variant="contained"
            color="primary"
            component={Link}
            to="/"
            size="large"
          >
            Back to Home
          </Button>

          <Button
            variant="outlined"
            color="primary"
            component={Link}
            to="/pathfinder"
            size="large"
          >
            Try Pathway Finder
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default NotFoundPage;
