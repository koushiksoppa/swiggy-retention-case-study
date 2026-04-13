# swiggy-retention-case-study
# 🍔 Swiggy User Retention — Product Case Study


---

## 📋 Table of Contents

- [Problem Definition](#1-problem-definition)
- [User Segmentation](#2-user-segmentation)
- [User Journey Map](#3-user-journey-map)
- [Pain Point Analysis](#4-pain-point-analysis)
- [Root Cause Analysis](#5-root-cause-analysis)
- [Product Solutions](#6-product-solutions)
- [Metrics to Track](#7-metrics-to-track)
- [Prioritization Framework](#8-prioritization-framework)
- [Final Recommendation](#9-final-recommendation)
- [Slide Deck Summary](#10-slide-deck-summary)
- [How to Use This Case Study](#how-to-use-this)

---

## 1. Problem Definition

### Problem Statement
> *"How might we improve the retention rate of Swiggy users beyond the initial discount-driven orders, to increase monthly order frequency and lifetime value — without solely relying on offers?"*

### Key Observations
- Swiggy **acquires users effectively** but loses them after 2–3 orders
- Retention drops sharply once the **discount/coupon honeymoon period** ends
- High CAC (~₹300–500/user) paired with low LTV = **broken unit economics**
- Estimated **30-day re-order rate drops 40–60%** after first promo expires

### Goals
| Goal | Target Metric |
|------|---------------|
| Improve habitual usage | Increase orders/user/month |
| Reduce churn | Improve D30 retention rate |
| Reduce discount dependency | Grow non-coupon order % |
| Improve experience quality | Raise post-order NPS |

---

## 2. User Segmentation

### Segment 1 — Discount Chasers 🔴
- Order **only when coupons are available**; high churn post-offer
- Typically new users, students, or price-sensitive demographics
- **Churn trigger:** Offer expires or competitor has a better deal
- **Retention lever:** Loyalty programs, value bundles, Swiggy One perks

### Segment 2 — Convenience Seekers 🟡
- Order **1–2x/week** for convenience (busy professionals, working couples)
- Drop off when delivery time is slow or food quality is inconsistent
- **Churn trigger:** 2–3 bad delivery experiences in a row
- **Retention lever:** Speed guarantees, Swiggy Bolt, reliable restaurant curation

### Segment 3 — Power Users 🟢
- Order **4+ times/week**; high LTV, likely Swiggy One subscribers
- Churn when personalization feels stale or app experience degrades
- **Churn trigger:** Better recommendation engine on a competitor app
- **Retention lever:** Personalization, exclusive benefits, gamification

### Segment 4 — Dormant Users 🔵
- Ordered **1–3 times, then went silent** (30+ days inactive)
- Often left due to a bad first experience or switched to Zomato
- **Churn trigger:** Single bad experience with no recovery
- **Retention lever:** Win-back campaigns, re-engagement nudges, personalized re-intro

---

## 3. User Journey Map

```
[1] Discovery
     └── Opens app / sees push notification or ad
          |
[2] Browse & Search
     └── Scrolls feed, searches cuisine or restaurant
          |
[3] Restaurant Selection
     └── Checks ratings, delivery time, menu photos
          |
[4] Cart Building
     └── Adds items, applies coupon, reviews total
          |
[5] Checkout & Payment
     └── Selects delivery address, chooses payment method
          |
[6] Live Tracking
     └── Watches real-time order status and delivery map
          |
[7] Delivery & Unboxing
     └── Receives food, checks order accuracy
          |
[8] Post-Order
     └── Rates food/delivery → Re-orders or churns
```

---

## 4. Pain Point Analysis

| Stage | Pain Point | Severity |
|-------|-----------|----------|
| Discovery | Generic push notifications; "order now" fatigue | 🟡 Medium |
| Browse & Search | Repetitive feed; hard to discover new restaurants | 🔴 High |
| Restaurant Selection | Inconsistent ratings; prep time not surfaced clearly | 🟡 Medium |
| Cart Building | Coupon confusion; hidden platform fees | 🔴 High |
| Checkout | Saved address errors; no ETA confidence at checkout | 🟡 Medium |
| Live Tracking | Inaccurate ETAs; no recourse when delays occur | 🔴 High |
| Delivery | Wrong/missing items; cold food; no easy resolution | 🔴 High |
| Post-Order | No follow-up nudge; slow refunds; no re-order shortcut | 🔴 High |

---

## 5. Root Cause Analysis

### RCA 1 — Discount Dependency 🔴
- Growth KPIs historically prioritized **acquisition over retention**
- Users are **trained to expect offers**; no non-discount value communicated
- No loyalty mechanic to create **switching costs**

### RCA 2 — Poor Personalization 🟡
- Feed shows same restaurants daily; **no context-awareness** (time of day, weather, past orders)
- Recommendations not updated fast enough after first few orders
- No proactive nudges like *"your usual?"* at the user's typical lunch hour

### RCA 3 — Inconsistent Delivery Experience 🟡
- ETA accuracy is low; **no proactive communication** on delays
- Issue resolution (wrong/missing items) takes too many steps and too long
- Post-bad-experience recovery is poor — **no automatic goodwill credits**

### RCA 4 — Weak Post-Order Engagement 🔵
- App engagement drops to **zero between orders**
- No content or social layer to build habit loops
- Re-order flow is buried in the UI; **no "repeat last order" shortcut** on the homescreen

---

## 6. Product Solutions

### P0 — Quick Wins (High Impact, Low Effort)

#### 6.1 Smart Re-order Widget
- **"Your usual?"** widget on homescreen — one-tap re-order of last 3 items at typical order time
- Contextual push notification: *"It's 1 PM on a weekday — your biryani place has 20 min delivery today"*
- Implementation: ML model on order history × time-of-day × day-of-week

#### 6.2 Proactive Issue Resolution
- **Auto-detect late orders** (>15 min past ETA) → proactively apply ₹30 credit — no user action needed
- **"Missing item?"** one-tap flow directly on the order tracking screen, resolved in <2 minutes
- Post-bad-experience re-engagement: *"We're sorry — here's ₹50 for your next order"* (auto-triggered)

---

### P1 — Big Bets (High Impact, High Effort)

#### 6.3 Contextual Personalization Engine
- Feed ranked by **time-of-day + weather + past order history** (not just restaurant popularity)
- **"Explore mode" toggle** — surfaces only restaurants the user has never ordered from
- **Restaurant health score** visible: *"98% accuracy last 30 days, avg 28 min delivery"*

#### 6.4 Swiggy One Lite — Low-friction Loyalty Tier
- **Free 30-day trial** triggered after user's 3rd order; frictionless upgrade with ₹ saved calculator
- **"Swiggy Coins"** earned per order, redeemable for delivery fee waiver (no minimum order threshold)
- Milestone unlocks: *"You've ordered 10 times — enjoy free delivery for a week"*
- **Weekly order streak tracker** with a small reward (₹20 credit at 4-week streak)

---

### P2 — Retention Boosters (Medium Impact, Medium Effort)

#### 6.5 Social & Content Layer
- **"What's trending near you"** feed — short food reels from partner restaurants
- **Share & earn:** Refer a dish to a friend, both get ₹30 off (non-discount habit hook)
- **Weekly "Food Wrapped"** — personalized stat card: *"You ordered biryani 11 times this month"*

---

## 7. Metrics to Track

### Primary Metrics
| Metric | Why It Matters |
|--------|---------------|
| **D30 retention rate** | Core health signal; % users who order again within 30 days |
| **Orders / user / month** | North Star — measures habit formation |
| **Re-order rate within 7 days** | Leading indicator of habit; faster feedback loop |

### Supporting Metrics
| Metric | Target |
|--------|--------|
| Churn rate by segment | Track discount chasers vs convenience vs power users separately |
| Issue resolution CSAT | % users satisfied with refund/delay handling → target >80% |
| Swiggy One conversion rate | Free trial → paid subscriber → target >15% |
| Feature adoption rate | % users using "Your usual?" widget within 30 days of launch |
| Average order value (AOV) | Ensure retention doesn't come at margin cost |

### Guardrail Metrics (Must Not Regress)
- Delivery partner satisfaction score
- Restaurant partner GMV distribution
- App crash rate / P99 load time

---

## 8. Prioritization Framework

### RICE Score Summary

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Re-order widget | High | High | High | Low | ⭐⭐⭐⭐⭐ |
| Auto-credit delays | High | High | High | Low | ⭐⭐⭐⭐⭐ |
| One-tap issue resolution | High | High | High | Low | ⭐⭐⭐⭐⭐ |
| Personalization engine | High | High | Medium | High | ⭐⭐⭐⭐ |
| Swiggy One Lite | Medium | High | Medium | High | ⭐⭐⭐⭐ |
| Streak + Coins gamification | Medium | Medium | Medium | Medium | ⭐⭐⭐ |
| Food Wrapped card | High | Low | High | Low | ⭐⭐ |
| Social content reels | Medium | Low | Low | High | ⭐ |

### Impact vs Effort Matrix

```
High Impact │ Quick Wins ✅      │  Big Bets 🎯
            │ · Re-order widget  │  · Personalization engine
            │ · Auto-credits     │  · Swiggy One Lite
            │ · Issue resolution │  · Streak gamification
────────────┼────────────────────┼──────────────────────────
Low Impact  │  Fill-ins 📌       │  Deprioritize ❌
            │ · Food Wrapped     │  · Social reels
            │ · Explore mode     │  · In-app communities
            │ · Health score     │  · Pre-placement orders
            │      Low Effort    │       High Effort
```

### Phased Roadmap

| Phase | Timeline | Focus |
|-------|----------|-------|
| Phase 1 | Month 1–2 | Quick wins: Re-order widget, auto-credits, one-tap issue resolution |
| Phase 2 | Month 3–4 | Big bets: Personalization engine v1, Swiggy One Lite free trial, streak system |
| Phase 3 | Month 5–6 | Scale: Gamification expansion, social referral, Food Wrapped launch |

---

## 9. Final Recommendation

### TL;DR
> Swiggy's retention problem is **not a pricing problem — it's a trust and habit problem.**  
> Fix the experience → Build the habit loop → Create switching costs.

### The 3-Step Strategy

1. **Fix trust first** — Auto-credits for delays and one-tap issue resolution rebuild user trust instantly. One bad delivery experience destroys 10 good ones. This is the highest-leverage, lowest-cost intervention.

2. **Build habit loops** — The "Your usual?" widget and order streaks are low-cost nudges that create the daily check-in habit, retaining users even without offers.

3. **Create switching costs** — A contextual personalization engine and a Swiggy One Lite loyalty tier reduce price sensitivity and make switching to Zomato feel costly over time.

### What to Avoid
- ❌ **Doubling down on coupons** — solves the symptom, worsens the root cause
- ❌ **Building social features before fixing core experience** — premature complexity
- ❌ **Optimizing only for GMV** — can be inflated by discounts while retention crumbles

### One-Line Interview Answer
> *"I'd prioritize fixing the bad-experience recovery loop first, then build a habit system via re-order shortcuts and streaks, and finally invest in personalization to make every session feel curated — so users return to Swiggy out of preference, not promotion."*

---

## 10. Slide Deck Summary

| Slide | Title | Key Points |
|-------|-------|-----------|
| 1 | Problem Definition | Discount dependency, broken unit economics, D30 retention drop |
| 2 | User Segments & Journey | 4 segments, 8-step journey, key drop-off points |
| 3 | Root Cause Analysis | Discount dependency, poor personalization, bad experience recovery |
| 4 | Product Solutions | P0 quick wins, P1 big bets, P2 boosters |
| 5 | Metrics & Prioritization | RICE framework, phased roadmap |
| 6 | Recommendation | Trust → Habit → Switching costs. Measure D30 + orders/month |

---

## How to Use This

This case study is structured for PM interviews. Here's how to use each section:

- **In a case interview:** Lead with Section 1 (problem) → 2 (segments) → 5 (RCA) → 6 (solutions) → 7 (metrics)
- **For a product sense question:** Use Sections 6 + 9
- **For a metrics question:** Use Section 7 directly
- **For prioritization questions:** Use Section 8 (RICE + matrix)
- **For execution/roadmap questions:** Use the phased roadmap in Section 8

---

## 📁 Repo Structure

```
swiggy-retention-case-study/
│
├── README.md                    ← This file (full case study)
├── slides/
│   └── slide-content.md         ← 6-slide deck content
├── frameworks/
│   ├── user-journey-map.md      ← Detailed journey map
│   ├── pain-points.md           ← Pain point deep dive
│   └── rice-scoring.md          ← RICE prioritization workings
└── resources/
    └── pm-interview-tips.md     ← How to present this in interviews
```

---
