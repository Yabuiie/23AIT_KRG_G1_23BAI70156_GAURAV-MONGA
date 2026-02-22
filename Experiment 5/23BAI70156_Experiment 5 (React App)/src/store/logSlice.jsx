import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

export const initialState = {
  data: [],
  status: "idle",
  error: null,
};

export const fetchLogs = createAsyncThunk(
  "logs/fetchLogs",
  async (_, { rejectWithValue }) => {
    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      return [
        { id: 1, activity: "Car Travel", carbon: 4 },
        { id: 2, activity: "Electricity Usage", carbon: 6 },
        { id: 3, activity: "Cycling", carbon: 0 },
      ];
    } catch (error) {
      return rejectWithValue("Failed to fetch logs");
    }
  }
);

const logsSlice = createSlice({
  name: "logs",
  initialState,
  reducers: {
    resetLogs: () => initialState,
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchLogs.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchLogs.fulfilled, (state, action) => {
        state.status = "success";
        state.data = action.payload;
      })
      .addCase(fetchLogs.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload || action.error.message;
      });
  },
});

export const { resetLogs } = logsSlice.actions;
export default logsSlice.reducer;