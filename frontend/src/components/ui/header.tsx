import Image from "next/image";
import { motion } from "framer-motion";

export function Header() {
  return (
    <motion.header
      className="w-full py-6 flex justify-center items-center"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center gap-3">
        <motion.div
          className="relative w-12 h-12"
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        >
          <Image
            src="/globe.svg"
            alt="Globetrotter Logo"
            fill
            className="object-contain"
          />
        </motion.div>
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-200 to-blue-400 bg-clip-text text-transparent">
            Globetrotter
          </h1>
          <p className="text-xs text-blue-300">Explore the world, one guess at a time</p>
        </motion.div>
      </div>
    </motion.header>
  );
}
