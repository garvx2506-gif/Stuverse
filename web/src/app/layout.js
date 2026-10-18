import "./globals.css";

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: "#050408",
};

export const metadata = {
  title: "Stuverse AI — Your Personal AI Teacher 🎓",
  description: "Ask any doubt, upload textbook questions & notes, and get step-by-step solutions in simple language with Stuverse AI.",
  keywords: ["AI Teacher", "Study Companion", "Homework Helper", "JEE", "NEET", "NCERT", "CBSE", "College", "Stuverse"],
  authors: [{ name: "Stuverse" }],
  openGraph: {
    title: "Stuverse AI — Your Personal AI Teacher 🎓",
    description: "Ask any doubt, upload textbook questions & notes, and get step-by-step solutions in simple language.",
    url: "https://stuverse.ai",
    siteName: "Stuverse AI",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Stuverse AI — Your Personal AI Teacher 🎓",
    description: "Ask any doubt, upload textbook questions & notes, and get step-by-step solutions in simple language.",
  },
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
