import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Loader from "@/components/ui/Loader";

const LoaderPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/itinerary");
    }, 3000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return <Loader />;
};

export default LoaderPage;
