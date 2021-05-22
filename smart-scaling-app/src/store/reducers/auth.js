import produce from "immer";

export const AUTH_START = "auth/START";
export const AUTH_SUCCESS = "auth/SUCCESS";
export const SIGNUP_SUCCESS = "auth/SIGNUP_SUCCESS";
export const LOGOUT = "auth/LOGOUT";
export const ERROR = "auth/ERROR";
export const RESET = "auth/RESET_SUCCESS_STATUS";

const initialState = {
  loading: false,
  object: null,
  success: false,
  error: null,
};

const reducer = produce((state, action) => {
  switch (action.type) {
    case AUTH_START:
      state.loading = true;
      break;

    case AUTH_SUCCESS:
      state.object = action.payload;
      state.loading = false;
      state.success = true;
      state.error = null;

      break;

    case SIGNUP_SUCCESS:
      state.loading = false;
      state.success = true;
      state.error = null;

      break;

    case ERROR:
      state.loading = false;
      state.error = action.payload;
      break;

    case LOGOUT:
      state.object = null;
      break;

    case RESET:
      state.success = false;
      break;

    default:
      return state;
  }
}, initialState);

export default reducer;
