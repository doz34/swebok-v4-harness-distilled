##### 18.2.4.1 Grouping and Aggregation

Step: GROUP BY

If the `GROUP BY` keyword is used, or there is implicit grouping due to the use of aggregates in the projection, then grouping is performed by the Group function. It divides the solution set into groups of one or more solutions, with the same overall cardinality. In case of implicit grouping, a fixed constant (1) is used to group all solutions into a single group.

Step: Aggregates

The aggregation step is applied as a transformation on the query level, replacing aggregate expressions in the query level with Aggregation() algebraic expressions.

The transformation for query levels that use any aggregates is given below:

```
Let A := the empty sequence
Let Q := the query level being evaluated
Let P := the algebra translation of the GroupGraphPattern of the query level
Let E := [], a list of pairs of the form (variable, expression)

If Q contains GROUP BY exprlist
   Let G := Group(exprlist, P)
Else If Q contains an aggregate in SELECT, HAVING, ORDER BY
   Let G := Group((1), P)
Else
   skip the rest of the aggregate step
   End

Global i := 1   # Initially 1 for each query processed

For each (X AS Var) in SELECT, each HAVING(X), and each ORDER BY X in Q
  For each unaggregated variable V in X
      Replace V with Sample(V)
      End
  For each aggregate R(args ; scalarvals) now in X
      # note scalarvals may be omitted, then it's equivalent to the empty set
      Ai := Aggregation(args, R, scalarvals, G)
      Replace R(...) with aggi in Q
      i := i + 1
      End
  End

For each variable V appearing outside of an aggregate
   Ai := Aggregation(V, Sample, {}, G)
   E := E append (V, aggi)
   i := i + 1
   End

A := Ai, ..., Ai-1
P := AggregateJoin(A)
```

Note: aggi is a temporary variable. E is then used in 18.2.4.4 for the processing of select expressions.

Example:

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT (SUM(?val) AS ?sum) (COUNT(?a) AS ?count)
WHERE {
  ?a rdf:value ?val .
} GROUP BY ?a
```

The SUM expression becomes agg1, and the COUNT expression becomes agg2.

```
Let G := Group((?a), BGP(?a rdf:value ?val))
A1 = Aggregation((?val), Sum, {}, G)
A2 = Aggregation((?a), Count, {}, G)
A := (A1, A2)
Let P := AggregateJoin(A)
```