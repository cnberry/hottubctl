# Research notes: Sundance SmartTub and local/direct control options

## Executive summary
For a Sundance spa, the most realistic control paths are:

1. **Keep SmartTub and use its cloud API**
   - Already proven viable enough for Home Assistant and `python-smarttub`
   - Best for quick wins
   - Not local
   - SmartTub appears to be **cellular-first**, not Wi‑Fi-first

2. **Board-level local control via RS-485 / network bridge**
   - Most promising long-term local/direct path
   - Requires identifying the spa control board and bus/accessory wiring
   - There is real community precedent for Sundance/Jacuzzi RS-485 integrations using bridges like **Elfin EW11/EW11A** or other RS-485-to-TCP devices

3. **Aftermarket Wi‑Fi module replacement only if compatible with your control pack**
   - Possible in some spa ecosystems
   - **Gecko in.touch 3/3+ is not a generic universal module**
   - It is designed for **Gecko control systems**, especially compatible Gecko in.yj / in.ye / in.yt family packs, not arbitrary Sundance packs
   - Unless your Sundance spa actually uses compatible Gecko hardware, this is probably the wrong module

## SmartTub findings
### Connectivity model
Sundance marketing and dealer pages repeatedly describe SmartTub as:
- a **cellular** control system
- using direct cellular connectivity rather than your home Wi‑Fi
- marketed specifically as more reliable outdoors than Wi‑Fi

That strongly suggests SmartTub is **not** the right substrate if your main goal is local network control.

### Practical implication
SmartTub is useful for:
- fast remote control
- diagnostics
- cloud integrations
- easy no-wiring deployment

But it is weak for:
- local-first automation
- direct LAN control
- independence from vendor cloud/service quality

### Cloud/API reality
There is still a meaningful cloud integration surface:
- Home Assistant has a built-in **SmartTub** integration
- open-source **`python-smarttub`** exists and already maps account/spa/status/config operations
- this gives a practical path for `hottubctl` today

If the goal is **usable soon**, SmartTub cloud remains the best short-term route.

## Gecko in.touch 3 / 3+ findings
### What it is
Gecko in.touch 3 / 3+ is a remote-control connectivity product for spas using **Gecko** control systems.

Vendor and reseller materials consistently describe compatibility with:
- Gecko **in.yj**
- Gecko **in.ye**
- Gecko **in.yt**
- and related Gecko families/versions

### Why this matters
That means the Gecko module is **controller-family specific**, not a general spa Wi‑Fi overlay you can bolt onto any Sundance spa.

### Bottom line on Gecko option
If your Sundance spa does **not** have a Gecko control pack, the Gecko in.touch 3+ is probably **not** the right answer.

So the Gecko module is only worth pursuing if we discover your spa/control board is actually Gecko-based, which is not the default assumption for Sundance/Jacuzzi-family tubs.

## Sundance/Jacuzzi local/direct-control research
### Most interesting clue
There is community work specifically for **Sundance/Jacuzzi** spas using:
- **RS-485**
- a **TCP/Wi‑Fi serial bridge** like **Elfin EW11 / EW11A**
- Home Assistant / MQTT integrations

Notably, there is a project explicitly describing:
- Sundance 780 series and other Jacuzzi products
- equipped with an **RS-485 to TCP COTS module such as Elfin 11**

This is important because it suggests:
- there is a real local bus worth tapping
- some Sundance/Jacuzzi systems are controllable or monitorable this way
- a local direct-control architecture is plausible without vendor cloud

### Why this path is attractive
If your tub has a usable RS-485/control bus, a local bridge path could give you:
- LAN-local control
- independence from SmartTub cloud
- a durable protocol-oriented solution
- better alignment with `*ctl` philosophy than cloud dependency

### What it requires
To evaluate this path properly, we need:
1. exact Sundance spa model/year/series
2. exact control board / pack model number
3. photos of the controller box and wiring labels
4. whether there is an exposed RS-485, accessory, or panel bus

Without that, we're still in informed-guess mode.

## Decision matrix
### Option A — Stay on SmartTub cloud
**Pros**
- fastest path to useful control
- already partially researched for `hottubctl`
- likely sufficient for temperature read/set

**Cons**
- cloud dependence
- cellular vendor lock-in
- weaker local automation story

### Option B — Add Gecko in.touch 3+
**Pros**
- Wi‑Fi remote control on compatible Gecko systems
- mature product in Gecko ecosystem

**Cons**
- likely incompatible with a non-Gecko Sundance controller
- risks being a dead-end purchase

**Current recommendation:** **do not buy this yet** unless we confirm Gecko compatibility.

### Option C — Build local bridge around Sundance/Jacuzzi control bus
**Pros**
- best local/direct-control story
- most UNIX-ish and durable
- avoids SmartTub cloud dependence

**Cons**
- most hardware investigation
- likely requires controller access, wiring review, and maybe a serial/network bridge

**Current recommendation:** best long-term direction if your spa hardware supports it.

## Best next steps
### Short-term best move
Use **SmartTub cloud** to get `hottubctl` working for temperature now.

### Parallel research move
Inspect the spa hardware for a potential local bus path:
- get spa model/year/series
- get control board part number
- get controller box photos
- identify any RS-485 or topside/accessory communications harness

### Purchase recommendation right now
If buying something today specifically for eventual local control, the best candidate is **not** the Gecko module yet.

A more defensible eventual buy would be something like:
- **Elfin EW11/EW11A** or similar RS-485-to-Wi‑Fi/TCP bridge

But only **after** confirming the Sundance controller actually exposes a compatible bus you can tap safely.

## Current answer to your question
- **SmartTub:** yes, it appears to be **cellular-first** rather than Wi‑Fi-first
- **Gecko in.touch 3+ (`0608-521041` / related family):** probably **not** the right module unless your Sundance hardware is secretly Gecko-compatible
- **Other workable solution:** the most promising local/direct path is likely **Sundance/Jacuzzi board-level RS-485 bridging**, not replacing SmartTub with Gecko

## Recommendation
### If you want something working fastest:
- continue with **SmartTub cloud** for `hottubctl`

### If you want the best local-first architecture:
- investigate the tub's **control board and RS-485/accessory bus**
- treat a local serial/network bridge as the leading candidate
- do **not** buy the Gecko module yet
