import React, { useState } from "react";
import {
  Alert,
  Autocomplete,
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Divider,
  Grid,
  InputAdornment,
  Paper,
  Slider,
  Step,
  StepContent,
  StepLabel,
  Stepper,
  TextField,
  Typography,
  useTheme,
  Tooltip,
} from "@mui/material";
import {
  Search as SearchIcon,
  ArrowForward as ArrowForwardIcon,
  Science as ScienceIcon,
  Route as RouteIcon,
} from "@mui/icons-material";
import { useMutation, useQuery } from "@tanstack/react-query";
import apiService, {
  Compound,
  PathInfo,
} from "../services/api";

const PathFinderPage: React.FC = () => {
  const theme = useTheme();
  const [startCompound, setStartCompound] = useState<string>("");
  const [endCompound, setEndCompound] = useState<string>("");
  const [maxSteps, setMaxSteps] = useState<number>(5);
  const [searchInitiated, setSearchInitiated] = useState(false);
  const [selectedPathIndex, setSelectedPathIndex] = useState(0);

  // Fetch compound suggestions for autocomplete
  const { data: compoundSuggestions = [], isLoading: suggestionsLoading } = useQuery<Compound[]>({
    queryKey: ["compoundSuggestions"],
    queryFn: () => apiService.getCompounds(),
    staleTime: 300000, // 5 minutes
  });

  // Find paths mutation
  const pathMutation = useMutation({
    mutationFn: () =>
      apiService.findPaths(startCompound, endCompound, maxSteps),
    onError: (error: any) => {
      console.error("Error finding paths:", error);
      // We'll handle the error display in the UI
    },
  });

  const findPaths = pathMutation.mutate;
  const pathResults = pathMutation.data;
  const pathsLoading = pathMutation.isPending;
  const pathError = pathMutation.error;
  const resetPathSearch = pathMutation.reset;

  // Handle search submission
  const handleSearch = () => {
    if (startCompound && endCompound) {
      setSearchInitiated(true);
      findPaths();
    }
  };

  // Reset search
  const handleReset = () => {
    setStartCompound("");
    setEndCompound("");
    setMaxSteps(5);
    setSearchInitiated(false);
    setSelectedPathIndex(0);
    resetPathSearch();
  };

  // Format reaction step for display
  const formatReactionStep = (reaction: any, index: number) => {
    return (
      <Box key={index}>
        <Typography variant="body1" gutterBottom>
          <strong>Reagent:</strong> {reaction.reagent}
        </Typography>
        {reaction.temperature && (
          <Typography variant="body2" color="textSecondary">
            <strong>Temperature:</strong> {reaction.temperature}
          </Typography>
        )}
        {reaction.pressure && (
          <Typography variant="body2" color="textSecondary">
            <strong>Pressure:</strong> {reaction.pressure} atm
          </Typography>
        )}
        {reaction.mechanism && (
          <Typography variant="body2" color="textSecondary">
            <strong>Mechanism:</strong> {reaction.mechanism}
          </Typography>
        )}
        {reaction.description && (
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            {reaction.description}
          </Typography>
        )}
      </Box>
    );
  };

  // Render path results
  const renderPathResults = () => {
    if (!pathResults || pathResults.length === 0) return null;

    const selectedPath = pathResults[selectedPathIndex];

    return (
      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Reaction Pathway Results
        </Typography>

        {/* Path selection */}
        {pathResults.length > 1 && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="body1" gutterBottom>
              Found {pathResults.length} possible pathways. Showing pathway{" "}
              {selectedPathIndex + 1}:
            </Typography>
            <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
              {pathResults.map((_, index) => (
                <Button
                  key={index}
                  variant={
                    selectedPathIndex === index ? "contained" : "outlined"
                  }
                  size="small"
                  onClick={() => setSelectedPathIndex(index)}
                >
                  Path {index + 1}
                </Button>
              ))}
            </Box>
          </Box>
        )}

        {/* Path summary */}
        <Paper
          elevation={0}
          sx={{
            p: 3,
            mb: 4,
            borderRadius: 2,
            border: `1px solid ${theme.palette.divider}`,
          }}
        >
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={8}>
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: 1,
                }}
              >
                {selectedPath.compounds.map(
                  (compound: Compound, index: number) => (
                    <React.Fragment key={index}>
                      <Tooltip
                        title={compound.properties?.name || ""}
                        placement="top"
                        arrow
                        disableHoverListener={!compound.properties?.name}
                      >
                        <Typography
                          variant="h6"
                          component="span"
                          sx={{
                            fontFamily: "monospace",
                            fontWeight: "bold",
                            color: theme.palette.primary.main,
                          }}
                        >
                          {compound.formula}
                        </Typography>
                      </Tooltip>
                      {index < selectedPath.compounds.length - 1 && (
                        <ArrowForwardIcon color="action" />
                      )}
                    </React.Fragment>
                  )
                )}
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: { xs: "left", md: "right" } }}>
                <Typography variant="body1">
                  <strong>Total Steps:</strong> {selectedPath.total_steps}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  <strong>Reagents:</strong> {selectedPath.reagents.join(", ")}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>

        {/* Step-by-step pathway */}
        <Typography variant="h6" gutterBottom>
          Step-by-Step Pathway
        </Typography>
        <Stepper orientation="vertical" sx={{ mb: 4 }}>
          {selectedPath.reactions.map((reaction: any, index: number) => (
            <Step key={index} active={true}>
              <StepLabel>
                <Typography variant="subtitle1">
                  Step {index + 1}: {selectedPath.compounds[index].formula} →{" "}
                  {selectedPath.compounds[index + 1].formula}
                </Typography>
                {selectedPath.compounds[index].properties?.name &&
                  selectedPath.compounds[index + 1].properties?.name && (
                    <Typography variant="body2" color="textSecondary">
                      {selectedPath.compounds[index].properties?.name} →{" "}
                      {selectedPath.compounds[index + 1].properties?.name}
                    </Typography>
                  )}
              </StepLabel>
              <StepContent>{formatReactionStep(reaction, index)}</StepContent>
            </Step>
          ))}
        </Stepper>
      </Box>
    );
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 3 }}>
        Chemical Pathway Finder
      </Typography>

      {/* Search Form */}
      <Paper
        elevation={0}
        sx={{
          p: 3,
          mb: 4,
          borderRadius: 2,
          border: `1px solid ${theme.palette.divider}`,
        }}
      >
        <Grid container spacing={3}>
          <Grid item xs={12} md={5}>
            <Autocomplete
              options={compoundSuggestions}
              getOptionLabel={(compound) => `${compound.name} (${compound.formula})`}
              value={compoundSuggestions.find((compound) => compound.id === startCompound) || null}
              onChange={(_, compound) => setStartCompound(compound?.id || "")}
              loading={suggestionsLoading}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Starting Compound"
                  placeholder="e.g., CH3CH2OH"
                  variant="outlined"
                  required
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <>
                        <InputAdornment position="start">
                          <ScienceIcon color="action" />
                        </InputAdornment>
                        {params.InputProps.startAdornment}
                      </>
                    ),
                    endAdornment: (
                      <>
                        {suggestionsLoading ? (
                          <CircularProgress color="inherit" size={20} />
                        ) : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
            />
          </Grid>

          <Grid
            item
            xs={12}
            md={2}
            sx={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <ArrowForwardIcon
              sx={{ fontSize: 40, color: theme.palette.text.secondary }}
            />
          </Grid>

          <Grid item xs={12} md={5}>
            <Autocomplete
              options={compoundSuggestions}
              getOptionLabel={(compound) => `${compound.name} (${compound.formula})`}
              value={compoundSuggestions.find((compound) => compound.id === endCompound) || null}
              onChange={(_, compound) => setEndCompound(compound?.id || "")}
              loading={suggestionsLoading}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Target Compound"
                  placeholder="e.g., CH3COOH"
                  variant="outlined"
                  required
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <>
                        <InputAdornment position="start">
                          <ScienceIcon color="action" />
                        </InputAdornment>
                        {params.InputProps.startAdornment}
                      </>
                    ),
                    endAdornment: (
                      <>
                        {suggestionsLoading ? (
                          <CircularProgress color="inherit" size={20} />
                        ) : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
            />
          </Grid>

          <Grid item xs={12}>
            <Typography gutterBottom>Maximum Steps: {maxSteps}</Typography>
            <Slider
              value={maxSteps}
              onChange={(_, newValue) => setMaxSteps(newValue as number)}
              min={1}
              max={6}
              step={1}
              marks
              valueLabelDisplay="auto"
            />
          </Grid>

          <Grid
            item
            xs={12}
            sx={{ display: "flex", justifyContent: "center", gap: 2, mt: 2 }}
          >
            <Button
              variant="contained"
              color="primary"
              size="large"
              startIcon={<SearchIcon />}
              onClick={handleSearch}
              disabled={!startCompound || !endCompound || pathsLoading}
            >
              Find Pathway
            </Button>
            <Button
              variant="outlined"
              color="primary"
              size="large"
              onClick={handleReset}
              disabled={pathsLoading}
            >
              Reset
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Loading indicator */}
      {pathsLoading && (
        <Box sx={{ display: "flex", justifyContent: "center", my: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Error message */}
      {pathError && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {pathError.message === "Request failed with status code 400" ||
          pathError.message === "Request failed with status code 404"
            ? "No reaction pathways found between these compounds. Try increasing the maximum steps or using different compounds."
            : pathError.message === "Network Error"
            ? "Unable to connect to the server. Please check your internet connection and try again."
            : "An error occurred while finding pathways. Please try again later."}
        </Alert>
      )}

      {/* No results message */}
      {searchInitiated &&
        !pathsLoading &&
        !pathError &&
        (!pathResults || pathResults.length === 0) && (
          <Alert severity="info" sx={{ mb: 4 }}>
            No reaction pathways found between these compounds. Try increasing
            the maximum steps or using different compounds.
          </Alert>
        )}

      {/* Results */}
      {renderPathResults()}
    </Container>
  );
};

export default PathFinderPage;
