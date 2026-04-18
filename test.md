Step 1: What's in a persistence diagram?
After running Ripser on your 50-day point cloud, you get a set of birth-death pairs for 1-cycles (loops):

$$\text{Dgm}_1 = {(b_1, d_1),\ (b_2, d_2),\ \ldots,\ (b_n, d_n)}$$

Each pair says: a loop appeared at radius $b_i$ and filled in (died) at radius $d_i$. The persistence of that loop is $d_i - b_i$ — how long it "lived."

A diagram with one very persistent loop looks like a point far above the diagonal. Noise looks like points clustered near the diagonal.

Step 2: The problem with diagrams
Diagrams are sets of points — you can't average them, add them, or plug them into standard statistics easily. You need to vectorize them.

Step 3: Persistence landscape
For each birth-death pair $(b_i, d_i)$, define a tent function:

$$\Lambda_i(t) = \begin{cases} t - b_i & \text{if } t \in [b_i,\tfrac{b_i+d_i}{2}] \\ d_i - t & \text{if } t \in [\tfrac{b_i+d_i}{2},\ d_i] \\ 0 & \text{otherwise} \end{cases}$$

It's a triangle that peaks at the midpoint $\tfrac{b_i+d_i}{2}$ with height $\tfrac{d_i - b_i}{2}$ (half the persistence). Long-lived loops → tall tents. Short-lived (noise) → tiny tents.

Now stack all the tent functions and take their pointwise maximum, then second maximum, etc.:

$$\lambda_k(t) = k\text{-th largest value among all } \Lambda_i(t)$$

The persistence landscape is the sequence of functions $\lambda_1, \lambda_2, \lambda_3, \ldots$

In practice $\lambda_1$ (the envelope of the tallest tents at each $t$) captures most of the signal.

Step 4: The L¹ norm
Once you have the landscape functions, the L¹ norm is just the area under them:

$$|\lambda|_1 = \sum_k \int |\lambda_k(t)|, dt$$

Since the tents are triangles, the area of each tent is:

$$\text{area} = \frac{1}{2} \cdot (d_i - b_i) \cdot \frac{d_i - b_i}{2} = \frac{(d_i - b_i)^2}{4}$$

So the L¹ norm is roughly the sum of squared persistences (up to a constant). Long-lived loops contribute a lot; short-lived noise contributes almost nothing.

Step 5: What Gidea & Katz actually track
Each trading day you have one diagram → one landscape → one L¹ number. Plot that number over time:

Normal market: loops are short-lived, L¹ stays low and stable
Pre-crash: the point cloud geometry gets more complex (correlated crash dynamics across indices create persistent loops), L¹ spikes
After crash: settles back down
The spike before 2008 appeared months before the Lehman collapse — that's the early warning signal.

Why landscapes over other vectorizations?
Two key reasons:

Statistical guarantees — Adams et al. (2017) proved a Law of Large Numbers and CLT for persistence landscapes, so you can do legitimate hypothesis testing
Stability — small changes in the diagram produce small changes in the landscape (L∞ stability inherited from diagram stability)