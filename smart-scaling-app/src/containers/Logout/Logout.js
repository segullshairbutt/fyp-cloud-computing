import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { Redirect } from "react-router";

import { logout } from "../../store/actions/authActions";

const Logout = (props) => {
  const dispatch = useDispatch();

  useEffect(() => dispatch(logout()), []);
  return <Redirect to="/" />;
};

export default Logout;
