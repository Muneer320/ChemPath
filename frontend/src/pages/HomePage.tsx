import React from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Grid,
  Paper,
  Typography,
  useTheme,
} from "@mui/material";
import {
  Science as ScienceIcon,
  Route as RouteIcon,
  School as SchoolIcon,
  Speed as SpeedIcon,
} from "@mui/icons-material";
import { Link } from "react-router-dom";

const HomePage: React.FC = () => {
  const theme = useTheme();

  const features = [
    {
      icon: <RouteIcon fontSize="large" color="primary" />,
      title: "Step-by-Step Pathways",
      description:
        "Explore short pathways between compounds in a small teaching graph.",
    },
    {
      icon: <ScienceIcon fontSize="large" color="primary" />,
      title: "Educational Focus",
      description:
        "A worked subset of organic conversions for classroom exploration.",
    },
    {
      icon: <SchoolIcon fontSize="large" color="primary" />,
      title: "Small teaching subset",
      description:
        "The 23 example variants are limited in scope; check your textbook for complete coverage and conditions.",
    },
    {
      icon: <SpeedIcon fontSize="large" color="primary" />,
      title: "Multiple Routes",
      description:
        "Compare distinct reagent variants and loop-free routes between selected compounds.",
    },
  ];

  return (
    <Container maxWidth="lg">
      {/* Hero Section */}
      <Paper
        elevation={0}
        sx={{
          p: 4,
          mt: 2,
          mb: 4,
          borderRadius: 2,
          background: `linear-gradient(120deg, ${theme.palette.primary.light}20, ${theme.palette.secondary.light}30)`,
          border: `1px solid ${theme.palette.primary.light}40`,
        }}
      >
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={7}>
            <Typography
              variant="h3"
              component="h1"
              gutterBottom
              fontWeight="bold"
            >
              ChemPath: Your Molecular GPS
            </Typography>
            <Typography variant="h6" color="textSecondary" paragraph>
              Navigate the complex world of chemical reactions with ease. Find
              example pathways between compounds in this limited teaching graph.
            </Typography>
            <Box sx={{ mt: 3 }}>
              <Button
                variant="contained"
                color="primary"
                size="large"
                component={Link}
                to="/pathfinder"
                sx={{ mr: 2, mb: { xs: 2, sm: 0 } }}
              >
                Try Pathway Finder
              </Button>
              <Button
                variant="outlined"
                color="primary"
                size="large"
                component={Link}
                to="/compounds"
              >
                Explore Compounds
              </Button>
            </Box>
          </Grid>
          <Grid
            item
            xs={12}
            md={5}
            sx={{ display: "flex", justifyContent: "center" }}
          >
            <Box
              component="img"
              src="/molecule.svg"
              alt="Molecule illustration"
              sx={{
                width: "100%",
                maxWidth: 300,
                display: { xs: "none", sm: "block" },
              }}
            />
          </Grid>
        </Grid>
      </Paper>

      {/* Features Section */}
      <Typography
        variant="h4"
        component="h2"
        gutterBottom
        align="center"
        sx={{ mb: 4 }}
      >
        Key Features
      </Typography>
      <Grid container spacing={3} sx={{ mb: 6 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              elevation={0}
              sx={{
                height: "100%",
                border: `1px solid ${theme.palette.divider}`,
                transition: "transform 0.3s, box-shadow 0.3s",
                "&:hover": {
                  transform: "translateY(-5px)",
                  boxShadow: "0 8px 16px rgba(0,0,0,0.1)",
                },
              }}
            >
              <CardContent sx={{ textAlign: "center", p: 3 }}>
                <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h6" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Example Section */}
      <Paper
        elevation={0}
        sx={{
          p: 3,
          mb: 4,
          borderRadius: 2,
          border: `1px solid ${theme.palette.divider}`,
        }}
      >
        <Typography variant="h5" component="h2" gutterBottom>
          Example: Converting Ethanol to Ethanoic Acid
        </Typography>
        <Typography variant="body1" paragraph>
          ChemPath explores short paths within its small teaching graph.
          For example, converting ethanol (CH₃CH₂OH) to ethanoic acid (CH₃COOH)
          can be done through multiple routes:
        </Typography>
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12} md={6}>
            <Card variant="outlined" sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Path 1: Oxidation Route
                </Typography>
                <Typography variant="body2" component="div">
                  <Box
                    component="span"
                    sx={{ fontFamily: "monospace", fontWeight: "bold" }}
                  >
                    CH₃CH₂OH → CH₃CHO → CH₃COOH
                  </Box>
                  <Box component="ul" sx={{ pl: 2, mt: 1 }}>
                    <li>Oxidation with K₂Cr₂O₇/H⁺</li>
                    <li>Further oxidation with K₂Cr₂O₇/H⁺</li>
                  </Box>
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Path 2: Alternative Route
                </Typography>
                <Typography variant="body2" component="div">
                  <Box
                    component="span"
                    sx={{ fontFamily: "monospace", fontWeight: "bold" }}
                  >
                    CH₃CH₂OH → CH₃CH₂Br → CH₃COOH
                  </Box>
                  <Box component="ul" sx={{ pl: 2, mt: 1 }}>
                    <li>Treatment with HBr</li>
                    <li>Nucleophilic substitution with KOH</li>
                    <li>Oxidation</li>
                  </Box>
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>

      {/* Call to Action */}
      <Box
        sx={{
          textAlign: "center",
          py: 4,
          mb: 2,
          borderRadius: 2,
          background: `linear-gradient(120deg, ${theme.palette.primary.light}20, ${theme.palette.secondary.light}30)`,
          border: `1px solid ${theme.palette.primary.light}40`,
          p: 4,
        }}
      >
        <Typography variant="h5" gutterBottom>
          Ready to simplify your chemistry studies?
        </Typography>
        <Typography variant="body1" paragraph>
          Start finding reaction pathways and ace your exams with confidence.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          size="large"
          component={Link}
          to="/pathfinder"
        >
          Get Started Now
        </Button>
      </Box>
    </Container>
  );
};

export default HomePage;
