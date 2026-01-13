import { motion } from "framer-motion";

export default function Button({ 
  children, 
  onClick, 
  className = "", 
  type = "button", 
  disabled = false,
  style = "primary"
}) {
  const baseStyles = "px-4 py-2 rounded font-medium transition-colors";
  
  const styleVariants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-500 text-white hover:bg-gray-600",
    danger: "bg-red-500 text-white hover:bg-red-600",
    success: "bg-green-500 text-white hover:bg-green-600",
    warning: "bg-yellow-500 text-white hover:bg-yellow-600",
  };

  return (
    <motion.button
      whileTap={{ scale: disabled ? 1 : 0.95 }}
      whileHover={{ scale: disabled ? 1 : 1.05 }}
      onClick={onClick}
      type={type}
      disabled={disabled}
      className={`${baseStyles} ${styleVariants[style] || styleVariants.primary} ${className} ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`}
    >
      {children}
    </motion.button>
  );
}

