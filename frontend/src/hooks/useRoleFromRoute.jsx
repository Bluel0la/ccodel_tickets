import { useLocation } from "react-router-dom";

const useRoleFromRoute = () => {
  const location = useLocation();
  const pathParts = location.pathname.split("/");

  // Define allowed roles
  const allowedRoles = ["student", "admin", "support"];

  if (pathParts.length >= 3 && pathParts[1] === "test" && allowedRoles.includes(pathParts[2])) {
    return pathParts[2]; // Return the valid role
  }

  return null; // Return null if the role is invalid or not found
};

export default useRoleFromRoute;
