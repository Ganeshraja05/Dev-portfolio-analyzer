import {
  Links,
  // LiveReload, // Comment out this line
  Outlet,
  Scripts,
  ScrollRestoration,
  useLoaderData,
} from "@remix-run/react";
import { json } from "@remix-run/node";
import NavBar from "./components/NavBar";

export const loader = async () => {
  return json({
    ENV: {
      API_URL: process.env.API_URL || "http://127.0.0.1:8000",
    },
  });
};

type LoaderData = {
  ENV: {
    API_URL: string;
  };
};

export default function App() {
  const { ENV } = useLoaderData<LoaderData>();
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <title>Portfolio Analyzer & Rater</title>
        <Links />
      </head>
      <body style={{ margin: 0, fontFamily: "Arial, sans-serif" }}>
        <NavBar />
        <div style={{ padding: "1rem" }}>
          <Outlet />
        </div>
        <ScrollRestoration />
        <Scripts />
        {/* <LiveReload /> */} {/* Comment out this line */}
        {/* Expose ENV variables to the browser */}
        <script
          dangerouslySetInnerHTML={{
            __html: `window.ENV = ${JSON.stringify(ENV)};`,
          }}
        />
      </body>
    </html>
  );
}