```tsx
export default function Page() {
  return (
    <main className="min-h-screen bg-background text-foreground">

      {/* Navbar */}
      <nav className="flex items-center justify-between border-b px-6 py-4 md:px-12">
        <div className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-primary-foreground">
            ⚡
          </div>

          <div>
            <h1 className="text-lg font-bold">EV Smart AI</h1>
            <p className="text-xs text-muted-foreground">
              Intelligent EV Management
            </p>
          </div>
        </div>

        <div className="hidden items-center gap-6 md:flex">
          <a href="#features" className="text-sm hover:text-primary">
            Features
          </a>

          <a href="#about" className="text-sm hover:text-primary">
            About
          </a>

          <a href="/dashboard">
            <button className="rounded-lg bg-primary px-5 py-2 text-sm text-primary-foreground">
              Dashboard
            </button>
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="flex min-h-[75vh] flex-col items-center justify-center px-6 text-center">

        <div className="mb-5 rounded-full border bg-muted px-4 py-2 text-sm">
          ⚡ AI-Powered Electric Vehicle Management
        </div>

        <h2 className="max-w-4xl text-4xl font-bold tracking-tight md:text-6xl">
          Smarter EV Management
          <span className="block text-muted-foreground">
            Powered by Artificial Intelligence
          </span>
        </h2>

        <p className="mt-6 max-w-2xl text-base leading-7 text-muted-foreground md:text-lg">
          Monitor electric vehicles, analyze traffic conditions, discover
          charging stations, optimize routes, and receive intelligent
          recommendations from one smart management platform.
        </p>

        <div className="mt-8 flex flex-col gap-4 sm:flex-row">

          <a href="/dashboard">
            <button className="rounded-xl bg-primary px-7 py-3 font-medium text-primary-foreground transition hover:opacity-90">
              Open Dashboard →
            </button>
          </a>

          <a href="#features">
            <button className="rounded-xl border px-7 py-3 font-medium transition hover:bg-muted">
              Explore Features
            </button>
          </a>

        </div>
      </section>

      {/* Features */}
      <section
        id="features"
        className="border-t bg-muted/30 px-6 py-20 md:px-12"
      >

        <div className="mx-auto max-w-6xl">

          <div className="mb-12 text-center">
            <p className="text-sm font-medium text-muted-foreground">
              SMART EV PLATFORM
            </p>

            <h2 className="mt-2 text-3xl font-bold">
              Everything You Need to Manage EVs
            </h2>

            <p className="mx-auto mt-4 max-w-2xl text-muted-foreground">
              Our system combines electric vehicle management, traffic
              information, charging infrastructure and AI-based recommendations.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

            {/* Feature 1 */}
            <div className="rounded-2xl border bg-card p-6 shadow-sm">
              <div className="mb-4 text-3xl">🚗</div>

              <h3 className="text-lg font-semibold">
                EV Tracking
              </h3>

              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Monitor electric vehicle information, location, status and
                important vehicle data.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="rounded-2xl border bg-card p-6 shadow-sm">
              <div className="mb-4 text-3xl">🔋</div>

              <h3 className="text-lg font-semibold">
                Battery Monitoring
              </h3>

              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Track EV battery status and receive useful information for
                efficient energy management.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="rounded-2xl border bg-card p-6 shadow-sm">
              <div className="mb-4 text-3xl">⚡</div>

              <h3 className="text-lg font-semibold">
                Charging Stations
              </h3>

              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Find charging stations and access charging-related information
                from the management dashboard.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="rounded-2xl border bg-card p-6 shadow-sm">
              <div className="mb-4 text-3xl">🗺️</div>

              <h3 className="text-lg font-semibold">
                Smart Route Planning
              </h3>

              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Plan routes while considering EV requirements, traffic
                conditions and charging availability.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="rounded-2xl border bg-card p-6 shadow-sm">
              <div className="mb-4 text-3xl">🚦</div>

              <h3 className="text-lg font-semibold">
                Traffic Management
              </h3>

              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Analyze traffic conditions to support better route selection
                and smarter transportation decisions.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="rounded-2xl border bg-card p-6 shadow-sm">
              <div className="mb-4 text-3xl">🤖</div>

              <h3 className="text-lg font-semibold">
                AI Recommendations
              </h3>

              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Use intelligent analysis to provide route, charging and EV
                management recommendations.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* About */}
      <section
        id="about"
        className="px-6 py-20 text-center md:px-12"
      >
        <div className="mx-auto max-w-3xl">

          <p className="text-sm font-medium text-muted-foreground">
            ABOUT THE PROJECT
          </p>

          <h2 className="mt-2 text-3xl font-bold">
            Building Smarter Electric Mobility
          </h2>

          <p className="mt-5 leading-7 text-muted-foreground">
            AI EV Management System is designed to combine electric vehicle
            monitoring, charging station management, traffic analysis and
            artificial intelligence into a single platform. The goal is to
            improve EV travel efficiency and provide users with intelligent,
            data-driven recommendations.
          </p>

        </div>
      </section>

      {/* Footer */}
      <footer className="border-t px-6 py-6 text-center text-sm text-muted-foreground">
        © 2026 AI EV Management System. Smart Mobility • Smart Energy • Smart Future
      </footer>

    </main>
  )
}
```
