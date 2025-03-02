import { motion } from "framer-motion";

export function Footer() {
  return (
    <motion.footer
      className="w-full py-4 mt-8 text-center text-blue-300 text-xs"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.8, duration: 0.5 }}
    >
      <p>© {new Date().getFullYear()} Globetrotter - Test your geography knowledge</p>
      <p className="mt-1">Made with ❤️ for explorers everywhere</p>
    </motion.footer>
  );
}
