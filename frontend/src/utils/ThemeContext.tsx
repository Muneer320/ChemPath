import React, {
  createContext,
  useState,
  useContext,
  useMemo,
  useEffect,
  ReactNode,
} from "react";
import {
  ThemeProvider as MuiThemeProvider,
  createTheme,
  PaletteMode,
  CssBaseline,
} from "@mui/material";

// Define the context type
interface ColorModeContextType {
  toggleColorMode: () => void;
  mode: PaletteMode;
}

// Create context with default values
const ColorModeContext = createContext<ColorModeContextType>({
  toggleColorMode: () => {},
  mode: "light",
});

// Custom hook to use the color mode context
export const useColorMode = () => useContext(ColorModeContext);

interface ThemeProviderProps {
  children: ReactNode;
}

// Theme provider component
export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  // Check for saved theme preference in localStorage
  const savedMode = localStorage.getItem("themeMode") as PaletteMode;
  const [mode, setMode] = useState<PaletteMode>(savedMode || "light");

  // Save theme preference to localStorage when it changes
  useEffect(() => {
    localStorage.setItem("themeMode", mode);
    document.body.setAttribute("data-theme", mode);
  }, [mode]);

  // Toggle between light and dark modes
  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
      },
      mode,
    }),
    [mode]
  );

  // Create theme based on current mode
  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          ...(mode === "light"
            ? {
                // Light mode palette
                primary: {
                  main: "#1976d2",
                  light: "#42a5f5",
                  dark: "#1565c0",
                },
                secondary: {
                  main: "#9c27b0",
                  light: "#ba68c8",
                  dark: "#7b1fa2",
                },
                background: {
                  default: "#f5f5f5",
                  paper: "#ffffff",
                },
                text: {
                  primary: "rgba(0, 0, 0, 0.87)",
                  secondary: "rgba(0, 0, 0, 0.6)",
                },
              }
            : {
                // Dark mode palette
                primary: {
                  main: "#90caf9",
                  light: "#e3f2fd",
                  dark: "#42a5f5",
                },
                secondary: {
                  main: "#ce93d8",
                  light: "#f3e5f5",
                  dark: "#ab47bc",
                },
                background: {
                  default: "#121212",
                  paper: "#1e1e1e",
                },
                text: {
                  primary: "#ffffff",
                  secondary: "rgba(255, 255, 255, 0.7)",
                },
              }),
        },
        components: {
          MuiPaper: {
            styleOverrides: {
              root: {
                transition: "background-color 0.3s ease",
              },
            },
          },
          MuiCard: {
            styleOverrides: {
              root: {
                boxShadow:
                  mode === "light"
                    ? "0 4px 6px rgba(0, 0, 0, 0.1)"
                    : "0 4px 6px rgba(0, 0, 0, 0.5)",
                transition: "box-shadow 0.3s ease, background-color 0.3s ease",
              },
            },
          },
          MuiButton: {
            styleOverrides: {
              root: {
                textTransform: "none",
              },
            },
          },
        },
      }),
    [mode]
  );

  return (
    <ColorModeContext.Provider value={colorMode}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ColorModeContext.Provider>
  );
};

export default ThemeProvider;
