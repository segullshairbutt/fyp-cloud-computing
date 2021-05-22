import Container from "@material-ui/core/Container";
import { Route } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { useEffect } from "react";

import ProjectList from "./containers/ProjectList";
import Swagger from "./containers/SwaggerUI";
import ProjectDetail from "./containers/ProjectDetail";
import Login from "./containers/Login/Login";
import Logout from "./containers/Logout/Logout";
import { checkToken } from "./store/actions/authActions";
import "./App.css";

function App() {
  const loggedIn = useSelector((state) => state.auth.object !== null);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(checkToken());
  }, []);

  return [
    <Container>
      <Route path="/:id/swagger/:filename" component={Swagger} />
      <Route exact path="/login" component={Login} />
      <Route
        exact
        path="/signup"
        render={(props) => <Login isSignup {...props} />}
      />
      <Route path="/logout" component={Logout} />
      {/* <ProjectDetail /> */}
      <Route exact path="/" component={ProjectList} />
      <Route exact path="/:id" component={ProjectDetail} />
    </Container>,
  ];
}

export default App;
