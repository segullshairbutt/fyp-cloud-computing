import axios from "../custom-axios";
import decode from "jwt-decode";
import {
  LOGOUT,
  SIGNUP_SUCCESS,
  AUTH_START,
  AUTH_SUCCESS,
  ERROR,
  RESET,
} from "../reducers/auth";

export const signup = (username, password) => {
  return (dispatch) => {
    dispatch({ type: AUTH_START });
    axios
      .post("/api/auth/signup", { username, password })
      .then((res) => {
        dispatch({ type: SIGNUP_SUCCESS });

        setTimeout(() => {
          dispatch({ type: RESET });
        }, 2000);
      })
      .catch((err) => {
        let errors = err?.response?.data?.errors;

        let errorMap = Object.values(errors).map((fieldValue) => fieldValue[0]);
        dispatch({ type: ERROR, payload: errorMap });
      });
  };
};

export const sendResetToken = (username, email) => {
  return (dispatch) => {
    dispatch({ type: AUTH_START });

    axios
      .post("/api/auth/forgot", { email, username })
      .then((res) => {
        dispatch({ type: SIGNUP_SUCCESS });

        setTimeout(() => {
          dispatch({ type: RESET });
        }, 2000);
      })
      .catch((err) => {
        console.log(err.response?.data);
        dispatch({ type: ERROR, payload: err.response.data?.error });
      });
  };
};

export const changePassword = (password, token) => {
  return (dispatch) => {
    dispatch({ type: AUTH_START });
    let data = {};
    let url = "/api/auth/change-password";

    if (token) {
      data = { password, token };
      url += "/token";
    } else {
      data = { password };
    }

    axios
      .put(url, data)
      .then(() => {
        dispatch({ type: AUTH_SUCCESS });

        setTimeout(() => {
          dispatch({ type: RESET });
        }, 2000);
      })
      .catch((err) => {
        console.log(err.response?.data);
        dispatch({ type: ERROR, payload: "Error during updating password." });
      });
  };
};

export const setToken = (token) => {
  return (dispatch) => {
    let decodedJwt = decode(token);
    let expiryDate = new Date(decodedJwt.exp * 1000);

    if (expiryDate <= new Date()) dispatch({ type: LOGOUT });
    else {
      setTimeout(() => {
        if (expiryDate <= new Date()) dispatch({ type: LOGOUT });
      }, 3600 * 1000);

      dispatch({ type: AUTH_SUCCESS, payload: decodedJwt });

      setTimeout(() => {
        dispatch({ type: RESET });
      }, 2000);
    }
  };
};

export const login = (username, password) => {
  return (dispatch) => {
    dispatch({ type: AUTH_START });
    axios
      .post("/api/auth/", { username, password })
      .then((res) => {
        localStorage.setItem("token", res.data.access);

        dispatch(setToken(res.data.access));
      })
      .catch((err) => {
        console.log(err);
        dispatch({ type: ERROR, payload: err?.response?.data?.detail });
      });
  };
};

export const checkToken = () => {
  return (dispatch) => {
    let token = localStorage.getItem("token");
    if (token) {
      dispatch(setToken(token));
    } else {
      dispatch(logout());
    }
  };
};

export const logout = () => {
  return (dispatch) => {
    localStorage.removeItem("token");
    localStorage.clear();
    dispatch({ type: LOGOUT });
  };
};
