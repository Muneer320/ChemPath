import React, { useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Container,
  Grid,
  InputAdornment,
  Paper,
  TextField,
  Typography,
  useTheme,
  CircularProgress,
  Alert,
  Pagination,
} from "@mui/material";
import { Search as SearchIcon } from "@mui/icons-material";
import { useQuery } from "@tanstack/react-query";
import apiService, { Compound } from "../services/api";

const CompoundsPage: React.FC = () => {
  const theme = useTheme();
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(1);
  const itemsPerPage = 12;

  // Fetch compounds with optional search term
  const {
    data: compounds,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["compounds", searchTerm],
    queryFn: () => apiService.getCompounds(searchTerm),
    staleTime: 60000, // 1 minute
  });

  // Handle search input change
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setPage(1); // Reset to first page on new search
  };

  // Calculate pagination
  const totalPages = compounds ? Math.ceil(compounds.length / itemsPerPage) : 0;
  const paginatedCompounds = compounds
    ? compounds.slice((page - 1) * itemsPerPage, page * itemsPerPage)
    : [];

  // Handle page change
  const handlePageChange = (
    event: React.ChangeEvent<unknown>,
    value: number
  ) => {
    setPage(value);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Format compound properties for display
  const formatCompoundProperties = (compound: Compound) => {
    const properties = compound.properties || {};
    return {
      name: properties.name || "Unknown",
      molecularWeight: properties.molecular_weight
        ? `${properties.molecular_weight} g/mol`
        : "N/A",
      state: properties.state || "N/A",
      class: properties.class || "N/A",
    };
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 3 }}>
        Chemical Compounds
      </Typography>

      {/* Search Bar */}
      <Paper
        elevation={0}
        sx={{
          p: 2,
          mb: 4,
          borderRadius: 2,
          border: `1px solid ${theme.palette.divider}`,
        }}
      >
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Search compounds by formula or name..."
          value={searchTerm}
          onChange={handleSearchChange}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon color="action" />
              </InputAdornment>
            ),
          }}
          sx={{ mb: isLoading ? 2 : 0 }}
        />
        {isLoading && (
          <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
            <CircularProgress size={24} />
          </Box>
        )}
      </Paper>

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Error loading compounds. Please try again later.
        </Alert>
      )}

      {/* Compounds Grid */}
      {compounds && compounds.length === 0 ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          No compounds found matching your search criteria.
        </Alert>
      ) : (
        <>
          <Grid container spacing={3} sx={{ mb: 4 }}>
            {paginatedCompounds.map((compound, index) => {
              const {
                name,
                molecularWeight,
                state,
                class: compoundClass,
              } = formatCompoundProperties(compound);

              return (
                <Grid item xs={12} sm={6} md={4} lg={3} key={compound.id}>
                  <Card
                    elevation={0}
                    sx={{
                      height: "100%",
                      border: `1px solid ${theme.palette.divider}`,
                      transition: "transform 0.2s, box-shadow 0.2s",
                      "&:hover": {
                        transform: "translateY(-4px)",
                        boxShadow: "0 6px 12px rgba(0,0,0,0.08)",
                      },
                    }}
                  >
                    <CardContent>
                      <Typography
                        variant="h6"
                        component="h2"
                        gutterBottom
                        sx={{
                          fontFamily: "monospace",
                          fontWeight: "bold",
                          color: theme.palette.primary.main,
                        }}
                      >
                        {compound.formula}
                      </Typography>
                      <Typography variant="subtitle1" gutterBottom>
                        {name}
                      </Typography>
                      <Box sx={{ mt: 2 }}>
                        <Typography
                          variant="body2"
                          color="textSecondary"
                          sx={{ mb: 0.5 }}
                        >
                          <strong>Molecular Weight:</strong> {molecularWeight}
                        </Typography>
                        <Typography
                          variant="body2"
                          color="textSecondary"
                          sx={{ mb: 0.5 }}
                        >
                          <strong>State:</strong> {state}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          <strong>Class:</strong> {compoundClass}
                        </Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              );
            })}
          </Grid>

          {/* Pagination */}
          {totalPages > 1 && (
            <Box sx={{ display: "flex", justifyContent: "center", mb: 4 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="primary"
                size="large"
                showFirstButton
                showLastButton
              />
            </Box>
          )}
        </>
      )}
    </Container>
  );
};

export default CompoundsPage;
