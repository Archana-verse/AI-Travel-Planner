import { Loader2 } from "lucide-react"; 
import React from "react";

const Loader = () => {
  return (
    <div className="flex justify-center items-center h-screen">
      <Loader2 className="animate-spin h-10 w-10 text-primary" />
    </div>
  );
};

export default Loader;
