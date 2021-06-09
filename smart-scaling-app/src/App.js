import Container from "@material-ui/core/Container";
import { Redirect, Route, Switch } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { useEffect } from "react";

import ProjectList from "./containers/ProjectList/ProjectList";
import Swagger from "./containers/SwaggerUI";
import ProjectDetail from "./containers/ProjectDetail/ProjectDetail";
import Navbar from "./components/Navbar/Navbar";
import Login from "./containers/Login/Login";
import Signup from "./containers/Signup/Signup";
import Logout from "./containers/Logout/Logout";
import ChangePassword from "./containers/ChangePassword/ChangePassword";
import ResetPassword from "./containers/ResetPassword/ResetPassword";
import { checkToken } from "./store/actions/authActions";
import "./App.css";

function App() {
  const loggedIn = useSelector((state) => state.auth.object !== null);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(checkToken());
  }, []);

  return [
    <Navbar auth={loggedIn} />,
    <Container>
      <Switch>
        <Route path="/login" component={Login} />

        <Route path="/signup" component={Signup} />
        <Route path="/change-tokenpwd" component={ChangePassword} />
        <Route path="/forgot" component={ResetPassword} />

        {loggedIn && (
          <Aux>
            <Route path="/change-password" component={ChangePassword} />
            <Route exact path="/:id" component={ProjectDetail} />
            <Route exact path="/" component={ProjectList} />
            <Route path="/logout" component={Logout} />
            <Route path="/:id/swagger/:filename" component={Swagger} />
          </Aux>
        )}
        <Route component={Login} />
      </Switch>
    </Container>,
  ];
}

export default App;

const Aux = (props) => props.children;
