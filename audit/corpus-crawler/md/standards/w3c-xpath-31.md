[https://www.w3.org/](https://www.w3.org/)

# XML Path Language (XPath) 3.1

## W3C Recommendation 21 March 2017

Status Update (6 April 2021): Feedback, comments, error reports on this specification should be sent via GitHub [https://github.com/w3c/qtspecs/issues](https://github.com/w3c/qtspecs/issues) or email to [public-qt-comments@w3.org](mailto:public-qt-comments@w3.org).
This version:
https://www.w3.org/TR/2017/REC-xpath-31-20170321/
Latest version of XPath 3.1:
https://www.w3.org/TR/xpath-31/
Previous versions of XPath 3.1:
https://www.w3.org/TR/2017/PR-xpath-31-20170117/

https://www.w3.org/TR/2016/CR-xpath-31-20161213/

https://www.w3.org/TR/2015/CR-xpath-31-20151217/

https://www.w3.org/TR/2014/CR-xpath-31-20141218/

https://www.w3.org/TR/2014/WD-xpath-31-20141007/

https://www.w3.org/TR/2014/WD-xpath-31-20140424/
Most recent version of XPath 3:
https://www.w3.org/TR/xpath-3/
Most recent version of XPath:
https://www.w3.org/TR/xpath/
Most recent Recommendation of XPath:
https://www.w3.org/TR/2014/REC-xpath-30-20140408/
Editors:
Jonathan Robie,
biblicalhumanities.org
<jonathan.robie@biblicalhumanities.org>
Michael Dyck, Invited Expert
<jmdyck@ibiblio.org>
Josh Spiegel, Oracle Corporation
<josh.spiegel@oracle.com>

Please check the [**errata**](https://www.w3.org/XML/2017/qt-errata/xpath-31-errata.html) for any errors or issues reported since publication.

See also [**translations**](https://www.w3.org/2003/03/Translations/byTechnology?technology=xquery-31).

This document is also available in these non-normative formats: [XML](https://www.w3.org/TR/2017/REC-xpath-31-20170321/xpath-31.xml) and [Change markings relative to previous edition](https://www.w3.org/TR/2017/REC-xpath-31-20170321/xpath-31-diff.html).

[Copyright](https://www.w3.org/Consortium/Legal/ipr-notice#Copyright) © 2017 [W3C](https://www.w3.org/)® ([MIT](https://www.csail.mit.edu/), [ERCIM](https://www.ercim.eu/), [Keio](https://www.keio.ac.jp/), [Beihang](http://ev.buaa.edu.cn/)). W3C [liability](https://www.w3.org/Consortium/Legal/ipr-notice#Legal_Disclaimer), [trademark](https://www.w3.org/Consortium/Legal/ipr-notice#W3C_Trademarks) and [document use](https://www.w3.org/Consortium/Legal/copyright-documents) rules apply.

---

## Abstract

XPath 3.1 is an expression language that allows the processing of values conforming to the data model defined in [XQuery and XPath Data Model (XDM) 3.1]. The name of the language derives from its most distinctive feature, the path expression, which provides a means of hierarchic addressing of the nodes in an XML tree. As well as modeling the tree structure of XML, the data model also includes atomic values, function items, and sequences. This version of XPath supports JSON as well as XML, adding maps and arrays to the data model and supporting them with new expressions in the language and new functions in [XQuery and XPath Functions and Operators 3.1]. These are the most important new features in XPath 3.1:

1. **3.11.1 Maps**.
2. **3.11.2 Arrays**.

XPath 3.1 is a superset of [XML Path Language (XPath) Version 3.0]. A detailed list of changes made since XPath 3.0 can be found in **I Change Log**.

## Status of this Document

*This section describes the status of this document at the time of its publication. Other documents may supersede this document. A list of current W3C publications and the latest revision of this technical report can be found in the [W3C technical reports index](https://www.w3.org/TR/) at https://www.w3.org/TR/.*

This document is governed by the [1 March 2017 W3C Process Document](https://www.w3.org/2017/Process-20170301/).

This is a [Recommendation](https://www.w3.org/2015/Process-20150901/#rec-publication) of the W3C.

This document was published by the W3C [XML Query Working Group](https://www.w3.org/XML/Query/) and the W3C [XSLT Working Group](https://www.w3.org/Style/XSL/), each of which is part of the [XML Activity](https://www.w3.org/XML/Activity).

This Recommendation specifies XPath version 3.1, a fully compatible extension of [XPath version 3.0](https://www.w3.org/TR/xpath-30/).

This specification is designed to be referenced normatively from other specifications defining a host language for it; it is not intended to be implemented outside a host language. The implementability of this specification has been tested in the context of its normative inclusion in host languages defined by the [XQuery 3.1](https://www.w3.org/TR/xquery-31/) and XSLT 3.0 (expected in 2017) specifications; see the [XQuery 3.1 implementation report](https://dev.w3.org/2011/QT3-test-suite/ReportingResults31/report.html) (and, in the future, the WGs expect that there will also be an XSLT 3.0 implementation report) for details.

No substantive changes have been made to this specification since its publication as a Proposed Recommendation.

Please report errors in this document using W3C's [public Bugzilla system](https://www.w3.org/Bugs/Public/) (instructions can be found at [https://www.w3.org/XML/2005/04/qt-bugzilla](https://www.w3.org/XML/2005/04/qt-bugzilla)). If access to that system is not feasible, you may send your comments to the W3C XSLT/XPath/XQuery public comments mailing list, [public-qt-comments@w3.org](mailto:public-qt-comments@w3.org). It will be very helpful if you include the string “[XPath31]” in the subject line of your report, whether made in Bugzilla or in email. Please use multiple Bugzilla entries (or, if necessary, multiple email messages) if you have more than one comment to make. Archives of the comments and responses are available at [https://lists.w3.org/Archives/Public/public-qt-comments/](https://lists.w3.org/Archives/Public/public-qt-comments/).

This document has been reviewed by W3C Members, by software developers, and by other W3C groups and interested parties, and is endorsed by the Director as a W3C Recommendation. It is a stable document and may be used as reference material or cited from another document. W3C's role in making the Recommendation is to draw attention to the specification and to promote its widespread deployment. This enhances the functionality and interoperability of the Web.

This document was produced by groups operating under the [5 February 2004 W3C Patent Policy](https://www.w3.org/Consortium/Patent-Policy-20040205/). W3C maintains a [public list of any patent disclosures (W3C XML Query Working Group)](https://www.w3.org/2004/01/pp-impl/18797/status#disclosures) and a [public list of any patent disclosures (W3C XSLT Working Group)](https://www.w3.org/2004/01/pp-impl/19552/status#disclosures) made in connection with the deliverables of each group; these pages also include instructions for disclosing a patent. An individual who has actual knowledge of a patent which the individual believes contains [Essential Claim(s)](https://www.w3.org/Consortium/Patent-Policy-20040205/#def-essential) must disclose the information in accordance with [section 6 of the W3C Patent Policy](https://www.w3.org/Consortium/Patent-Policy-20040205/#sec-Disclosure).

## Table of Contents

1. 1Introduction
2. 2Basics 2.1Expression Context2.1.1Static Context 2.1.2Dynamic Context 2.2Processing Model2.2.1Data Model Generation 2.2.2Schema Import Processing 2.2.3Expression Processing2.2.3.1Static Analysis Phase 2.2.3.2Dynamic Evaluation Phase 2.2.4Consistency Constraints 2.3Error Handling2.3.1Kinds of Errors 2.3.2Identifying and Reporting Errors 2.3.3Handling Dynamic Errors 2.3.4Errors and Optimization 2.4Concepts2.4.1Document Order 2.4.2Atomization 2.4.3Effective Boolean Value 2.4.4Input Sources 2.4.5URI Literals 2.4.6Resolving a Relative URI Reference 2.5Types2.5.1Predefined Schema Types 2.5.2Namespace-sensitive Types 2.5.3Typed Value and String Value 2.5.4SequenceType Syntax 2.5.5SequenceType Matching2.5.5.1Matching a SequenceType and a Value 2.5.5.2Matching an ItemType and an Item 2.5.5.3Element Test 2.5.5.4Schema Element Test 2.5.5.5Attribute Test 2.5.5.6Schema Attribute Test 2.5.5.7Function Test 2.5.5.8Map Test 2.5.5.9Array Test 2.5.6SequenceType Subtype Relationships2.5.6.1The judgement subtype(A, B) 2.5.6.2The judgement subtype-itemtype(Ai, Bi) 2.5.7xs:error 2.6Comments
3. 3Expressions 3.1Primary Expressions3.1.1Literals 3.1.2Variable References 3.1.3Parenthesized Expressions 3.1.4Context Item Expression 3.1.5Static Function Calls3.1.5.1Evaluating Static and Dynamic Function Calls 3.1.5.2Function Conversion Rules 3.1.5.3Function Coercion 3.1.6Named Function References 3.1.7Inline Function Expressions 3.1.8Enclosed Expressions 3.2Postfix Expressions3.2.1Filter Expressions 3.2.2Dynamic Function Calls 3.3Path Expressions3.3.1Relative Path Expressions3.3.1.1Path operator (/) 3.3.2Steps3.3.2.1Axes 3.3.2.2Node Tests 3.3.3Predicates within Steps 3.3.4Unabbreviated Syntax 3.3.5Abbreviated Syntax 3.4Sequence Expressions3.4.1Constructing Sequences 3.4.2Combining Node Sequences 3.5Arithmetic Expressions 3.6String Concatenation Expressions 3.7Comparison Expressions3.7.1Value Comparisons 3.7.2General Comparisons 3.7.3Node Comparisons 3.8Logical Expressions 3.9For Expressions 3.10Let Expressions 3.11Maps and Arrays3.11.1Maps3.11.1.1Map Constructors 3.11.1.2Map Lookup using Function Call Syntax 3.11.2Arrays3.11.2.1Array Constructors 3.11.2.2Array Lookup using Function Call Syntax 3.11.3The Lookup Operator ("?") for Maps and Arrays3.11.3.1Unary Lookup 3.11.3.2Postfix Lookup 3.12Conditional Expressions 3.13Quantified Expressions 3.14Expressions on SequenceTypes3.14.1Instance Of 3.14.2Cast 3.14.3Castable 3.14.4Constructor Functions 3.14.5Treat 3.15Simple map operator (!) 3.16Arrow operator (=>)
4. 4Conformance 4.1Static Typing Feature
5. AXPath 3.1 Grammar A.1EBNFA.1.1Notation A.1.2Extra-grammatical Constraints A.1.3Grammar Notes A.2Lexical structureA.2.1Terminal Symbols A.2.2Terminal Delimitation A.2.3End-of-Line HandlingA.2.3.1XML 1.0 End-of-Line Handling A.2.3.2XML 1.1 End-of-Line Handling A.2.4Whitespace RulesA.2.4.1Default Whitespace Handling A.2.4.2Explicit Whitespace Handling A.3Reserved Function Names A.4Precedence Order (Non-Normative)
6. BType Promotion and Operator Mapping B.1Type Promotion B.2Operator Mapping
7. CContext Components C.1Static Context Components C.2Dynamic Context Components
8. DImplementation-Defined Items
9. EReferences E.1Normative References E.2Non-normative References E.3Background Material
10. FError Conditions
11. GGlossary (Non-Normative)
12. HBackwards Compatibility (Non-Normative) H.1Incompatibilities relative to XPath 3.0 H.2Incompatibilities relative to XPath 2.0 H.3Incompatibilities relative to XPath 1.0H.3.1Incompatibilities when Compatibility Mode is true H.3.2Incompatibilities when Compatibility Mode is false H.3.3Incompatibilities when using a Schema
13. IChange Log (Non-Normative) I.1Changes since the Candidate Recommendation of 17 December 2015I.1.1Substantive Changes I.1.2Editorial Changes I.2Changes introduced in the Candidate Recommendation of 17 December 2015I.2.1Substantive Changes I.2.2Editorial Changes I.3Changes introduced in the Candidate Recommendation of 18 December 2014I.3.1Substantive Changes I.3.2Editorial Changes I.4Changes introduced in prior Working Drafts

---

## 1 Introduction

The primary purpose of XPath is to address the nodes of XML trees and JSON trees. XPath gets its name from its use of a path notation for navigating through the hierarchical structure of an XML document. XPath uses a compact, non-XML syntax to facilitate use of XPath within URIs and XML attribute values. XPath 3.1 adds a similar syntax for navigating JSON trees.

[Definition: XPath 3.1 operates on the abstract, logical structure of an XML document or JSON object, rather than its surface syntax. This logical structure, known as the **data model**, is defined in [XQuery and XPath Data Model (XDM) 3.1].]

XPath is designed to be embedded in a host language such as [XSL Transformations (XSLT) Version 3.0] or [XQuery 3.1: An XML Query Language]. [Definition: A **host language** for XPath is a language or specification that incorporates XPath as a sublanguage and that defines how the static and dynamic context for evaluation of XPath expressions are to be established.]

XPath 3.1 is a subset of XQuery 3.1. In general, any expression that is syntactically valid and executes successfully in both XPath 3.1 and XQuery 3.1 will return the same result in both languages. There are a few exceptions to this rule:

- Because XQuery expands predefined entity references and character references and XPath does not, expressions containing these produce different results in the two languages. For instance, the value of the string literal `"&amp;"` is `&` in XQuery, and `&amp;` in XPath. (XPath is often embedded in other languages, which may expand predefined entity references or character references before the XPath expression is evaluated.)
- If XPath 1.0 compatibility mode is enabled, XPath behaves differently from XQuery in a number of ways, which are noted throughout this document, and listed in **H.3.2 Incompatibilities when Compatibility Mode is false**.

Because these languages are so closely related, their grammars and language descriptions are generated from a common source to ensure consistency, and the editors of these specifications work together closely.

XPath 3.1 also depends on and is closely related to the following specifications:

- [XQuery and XPath Data Model (XDM) 3.1] defines the data model that underlies all XPath 3.1 expressions.
- The type system of XPath 3.1 is based on XML Schema. It is implementation-defined whether the type system is based on [XML Schema 1.0] or [XML Schema 1.1].
- The built-in function library and the operators supported by XPath 3.1 are defined in [XQuery and XPath Functions and Operators 3.1].

This document specifies a grammar for XPath 3.1, using the same basic EBNF notation used in [XML 1.0]. Unless otherwise noted (see **A.2 Lexical structure**), whitespace is not significant in expressions. Grammar productions are introduced together with the features that they describe, and a complete grammar is also presented in the appendix [**A XPath 3.1 Grammar**]. The appendix is the normative version.

In the grammar productions in this document, named symbols are underlined and literal text is enclosed in double quotes. For example, the following productions describe the syntax of a static function call:

| [63]                                  | `FunctionCall`                        | ::=                                   | ` EQName ArgumentList `               | */* xgc: reserved-function-names */*  |
| ------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- |
|                                       |                                       |                                       |                                       | */* gn: parens */*                    |
| [50]                                  | `ArgumentList`                        | ::=                                   | `"(" (Argument ("," Argument)*)? ")"` |                                       |

The productions should be read as follows: A function call consists of an EQName followed by an ArgumentList. The argument list consists of an opening parenthesis, an optional list of one or more arguments (separated by commas), and a closing parenthesis.

This document normatively defines the static and dynamic semantics of XPath 3.1. In this document, examples and material labeled as "Note" are provided for explanatory purposes and are not normative.

Certain aspects of language processing are described in this specification as **implementation-defined** or **implementation-dependent**.

- [Definition: **Implementation-defined** indicates an aspect that may differ between implementations, but must be specified by the implementor for each particular implementation.]
- [Definition: **Implementation-dependent** indicates an aspect that may differ between implementations, is not specified by this or any W3C specification, and is not required to be specified by the implementor for any particular implementation.]

A language aspect described in this specification as **implementation-defined** or **implementation dependent** may be further constrained by the specifications of a host language in which XPath is embedded.

## 2 Basics

The basic building block of XPath 3.1 is the **expression**, which is a string of [Unicode] characters; the version of Unicode to be used is implementation-defined. The language provides several kinds of expressions which may be constructed from keywords, symbols, and operands. In general, the operands of an expression are other expressions. XPath 3.1 allows expressions to be nested with full generality.

**Note:**

This specification contains no assumptions or requirements regarding the character set encoding of strings of [Unicode] characters.

Like XML, XPath 3.1 is a case-sensitive language. Keywords in XPath 3.1 use lower-case characters and are not reserved—that is, names in XPath 3.1 expressions are allowed to be the same as language keywords, except for certain unprefixed function-names listed in **A.3 Reserved Function Names**.

[Definition: In the data model, a **value** is always a sequence.] [Definition: A **sequence** is an ordered collection of zero or more items.] [Definition: An **item** is either an atomic value, a node, or a [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31.] [Definition: An **atomic value** is a value in the value space of an **atomic type**, as defined in [XML Schema 1.0] or [XML Schema 1.1].] [Definition: A **node** is an instance of one of the **node kinds** defined in [Section 6 Nodes](https://www.w3.org/TR/xpath-datamodel-31/#Node)DM31.] Each node has a unique **node identity**, a **typed value**, and a **string value**. In addition, some nodes have a **name**. The **typed value** of a node is a sequence of zero or more atomic values. The **string value** of a node is a value of type `xs:string`. The **name** of a node is a value of type `xs:QName`.

[Definition: A sequence containing exactly one item is called a **singleton**.] An item is identical to a singleton sequence containing that item. Sequences are never nested—for example, combining the values 1, (2, 3), and ( ) into a single sequence results in the sequence (1, 2, 3). [Definition: A sequence containing zero items is called an **empty sequence**.]

[Definition: The term **XDM instance** is used, synonymously with the term value, to denote an unconstrained sequence of items.]

Element nodes have a property called **in-scope namespaces**. [Definition: The **in-scope namespaces** property of an element node is a set of namespace bindings, each of which associates a namespace prefix with a URI.] For a given element, one namespace binding may have an empty prefix; the URI of this namespace binding is the default namespace within the scope of the element.

In [XML Path Language (XPath) Version 1.0], the in-scope namespaces of an element node are represented by a collection of **namespace nodes** arranged on a **namespace axis**. As of XPath 2.0, the namespace axis is deprecated and need not be supported by a host language. A host language that does not support the namespace axis need not represent namespace bindings in the form of nodes.

[Definition: An **expanded QName** is a triple: its components are a prefix, a local name, and a namespace URI. In the case of a name in no namespace, the namespace URI and prefix are both absent. In the case of a name in the default namespace, the prefix is absent.] When comparing two expanded QNames, the prefixes are ignored: the local name parts must be equal under the Unicode Codepoint Collation, and the namespace URI parts must either both be absent, or must be equal under the Unicode Codepoint Collation.

In the XPath grammar, QNames representing the names of elements, attributes, functions, variables, types, or other such constructs are written as instances of the grammatical production EQName.

| [112]                                                    | `EQName`                                                 | ::=                                                      | ` QName \| URIQualifiedName `                            |                                                          |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| [122]                                                    | `QName`                                                  | ::=                                                      | ` [http://www.w3.org/TR/REC-xml-names/#NT-QName]Names `  | */* xgc: xml-version */*                                 |
| [123]                                                    | `NCName`                                                 | ::=                                                      | ` [http://www.w3.org/TR/REC-xml-names/#NT-NCName]Names ` | */* xgc: xml-version */*                                 |
| [117]                                                    | `URIQualifiedName`                                       | ::=                                                      | ` BracedURILiteral NCName `                              | */* ws: explicit */*                                     |
| [118]                                                    | `BracedURILiteral`                                       | ::=                                                      | `"Q" "{" [^{}]* "}"`                                     | */* ws: explicit */*                                     |

The EQName production allows a QName to be written in one of three ways:

- local-name only (for example, `invoice`). A name written in this form has no prefix, and the rules for determining the namespace depend on the context in which the name appears. This form is a lexical QName.
- prefix plus local-name (for example, `my:invoice`). In this case the prefix and local name of the QName are as written, and the namespace URI is inferred from the prefix by examining the in-scope namespaces in the static context where the QName appears; the context must include a binding for the prefix. This form is a lexical QName.
- URI plus local-name (for example, `Q{http://example.com/ns}invoice)`. In this case the local name and namespace URI are as written, and the prefix is absent. This way of writing a QName is context-free, which makes it particularly suitable for use in expressions that are generated by software. This form is a URIQualifiedName. If the BracedURILiteral has no content (for example, `Q{}invoice`) then the namespace URI of the QName is absent.

[Definition: A **lexical QName** is a name that conforms to the syntax of the QName production].

The namespace URI value in a URIQualifiedName is whitespace normalized according to the rules for the `xs:anyURI` type in [Section 3.2.17 anyURI](https://www.w3.org/TR/xmlschema-2/#anyURI)XS1-2 or [Section 3.3.17 anyURI](https://www.w3.org/TR/xmlschema11-2/#anyURI)XS11-2. It is a static error [err:XQST0070] if the namespace URI for an EQName is `http://www.w3.org/2000/xmlns/`.

Here are some examples of EQNames:

- `pi` is a lexical QName without a namespace prefix.
- `math:pi` is a lexical QName with a namespace prefix.
- `Q{http://www.w3.org/2005/xpath-functions/math}pi` specifies the namespace URI using a BracedURILiteral; it is not a lexical QName.

This document uses the following namespace prefixes to represent the namespace URIs with which they are listed. Although these prefixes are used within this specification to refer to the corresponding namespaces, not all of these bindings will necessarily be present in the static context of every expression, and authors are free to use different prefixes for these namespaces, or to bind these prefixes to different namespaces.

- `xs = http://www.w3.org/2001/XMLSchema`
- `fn = http://www.w3.org/2005/xpath-functions`
- `map = http://www.w3.org/2005/xpath-functions/map`
- `array = http://www.w3.org/2005/xpath-functions/array`
- `math = http://www.w3.org/2005/xpath-functions/math`
- `err = http://www.w3.org/2005/xqt-errors` (see **2.3.2 Identifying and Reporting Errors**).

[Definition: Within this specification, the term **URI** refers to a Universal Resource Identifier as defined in [RFC3986] and extended in [RFC3987] with the new name **IRI**.] The term URI has been retained in preference to IRI to avoid introducing new names for concepts such as "Base URI" that are defined or referenced across the whole family of XML specifications.

**Note:**

In most contexts, processors are not required to raise errors if a URI is not lexically valid according to [RFC3986] and [RFC3987]. See **2.4.5 URI Literals** for details.

### 2.1 Expression Context

[Definition: The **expression context** for a given expression consists of all the information that can affect the result of the expression.]

This information is organized into two categories called the static context and the dynamic context.

#### 2.1.1 Static Context

[Definition: The **static context** of an expression is the information that is available during static analysis of the expression, prior to its evaluation.] This information can be used to decide whether the expression contains a static error.

The individual components of the static context are described below. A default initial value for each component must be specified by the host language. The scope of each component is specified in **C.1 Static Context Components**.

- [Definition: **XPath 1.0 compatibility mode.** This value is `true` if rules for backward compatibility with XPath Version 1.0 are in effect; otherwise it is `false`. ]
- [Definition: **Statically known namespaces.** This is a mapping from prefix to namespace URI that defines all the namespaces that are known during static processing of a given expression.] The URI value is whitespace normalized according to the rules for the `xs:anyURI` type in [Section 3.2.17 anyURI](https://www.w3.org/TR/xmlschema-2/#anyURI)XS1-2 or [Section 3.3.17 anyURI](https://www.w3.org/TR/xmlschema11-2/#anyURI)XS11-2. Note the difference between in-scope namespaces, which is a dynamic property of an element node, and statically known namespaces, which is a static property of an expression.
- [Definition: **Default element/type namespace.** This is a namespace URI or [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31. The namespace URI, if present, is used for any unprefixed QName appearing in a position where an element or type name is expected.] The URI value is whitespace normalized according to the rules for the `xs:anyURI` type in [Section 3.2.17 anyURI](https://www.w3.org/TR/xmlschema-2/#anyURI)XS1-2 or [Section 3.3.17 anyURI](https://www.w3.org/TR/xmlschema11-2/#anyURI)XS11-2.
- [Definition: **Default function namespace.** This is a namespace URI or [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31. The namespace URI, if present, is used for any unprefixed QName appearing in a position where a function name is expected.] The URI value is whitespace normalized according to the rules for the `xs:anyURI` type in [Section 3.2.17 anyURI](https://www.w3.org/TR/xmlschema-2/#anyURI)XS1-2 or [Section 3.3.17 anyURI](https://www.w3.org/TR/xmlschema11-2/#anyURI)XS11-2.
- [Definition: **In-scope schema definitions.** This is a generic term for all the element declarations, attribute declarations, and schema type definitions that are in scope during static analysis of an expression.] It includes the following three parts: [Definition: **In-scope schema types.** Each schema type definition is identified either by an expanded QName (for a **named type**) or by an implementation-dependent type identifier (for an **anonymous type**). The in-scope schema types include the predefined schema types described in **2.5.1 Predefined Schema Types**. ] [Definition: **In-scope element declarations.** Each element declaration is identified either by an expanded QName (for a top-level element declaration) or by an implementation-dependent element identifier (for a local element declaration). ] An element declaration includes information about the element's substitution group affiliation. [Definition: **Substitution groups** are defined in [Section 2.2.2.2 Element Substitution Group](https://www.w3.org/TR/xmlschema-1/#Element_Equivalence_Class)XS1-1 and [Section 2.2.2.2 Element Substitution Group](https://www.w3.org/TR/xmlschema11-1/#Element_Equivalence_Class)XS11-1. Informally, the substitution group headed by a given element (called the **head element**) consists of the set of elements that can be substituted for the head element without affecting the outcome of schema validation.] [Definition: **In-scope attribute declarations.** Each attribute declaration is identified either by an expanded QName (for a top-level attribute declaration) or by an implementation-dependent attribute identifier (for a local attribute declaration). ]
- [Definition: **In-scope variables.** This is a mapping from expanded QName to type. It defines the set of variables that are available for reference within an expression. The expanded QName is the name of the variable, and the type is the static type of the variable.] An expression that binds a variable extends the in-scope variables, within the scope of the variable, with the variable and its type. Within the body of an inline function expression , the in-scope variables are extended by the names and types of the **function parameters**.
- [Definition: **Context item static type.** This component defines the static type of the context item within the scope of a given expression.]
- [Definition: **Statically known function signatures.** This is a mapping from (expanded QName, arity) to [function signature](https://www.w3.org/TR/xpath-datamodel-31/#dt-signature)DM31. ] The entries in this mapping define the set of functions that are available to be called from a static function call, or referenced from a named function reference. Each such function is uniquely identified by its expanded QName and arity (number of parameters). Given a statically known function's expanded QName and arity, this component supplies the function's [signature](https://www.w3.org/TR/xpath-datamodel-31/#dt-signature)DM31, which specifies various static properties of the function, including types. The statically known function signatures include the signatures of functions from a variety of sources, including the built-in functions. Implementations must ensure that no two functions have the same expanded QName and the same arity (even if the signatures are consistent).
- [Definition: **Statically known collations.** This is an implementation-defined mapping from URI to collation. It defines the names of the collations that are available for use in processing expressions.] [Definition: A **collation** is a specification of the manner in which strings and URIs are compared and, by extension, ordered. For a more complete definition of collation, see [Section 5.3 Comparison of strings](https://www.w3.org/TR/xpath-functions-31/#string-compare)FO31.]
- [Definition: **Default collation.** This identifies one of the collations in statically known collations as the collation to be used by functions and operators for comparing and ordering values of type `xs:string` and `xs:anyURI` (and types derived from them) when no explicit collation is specified.]
- [Definition: **Static Base URI.** This is an absolute URI, used to resolve relative URI references. ] If E is a subexpression of F then the Static Base URI of E is the same as the Static Base URI of F. There are no constructs in XPath that require resolution of relative URI references during static analysis. The Static Base URI is available during dynamic evaluation by use of the `fn:static-base-uri` function, and is used implicitly during dynamic evaluation by functions such as `fn:doc`. Relative URI references are resolved as described in **2.4.6 Resolving a Relative URI Reference**.
- [Definition: **Statically known documents.** This is a mapping from strings to types. The string represents the absolute URI of a resource that is potentially available using the `fn:doc` function. The type is the static type of a call to `fn:doc` with the given URI as its literal argument. ] If the argument to `fn:doc` is a string literal that is not present in **statically known documents**, then the static type of `fn:doc` is `document-node()?`. **Note:** The purpose of the **statically known documents** is to provide static type information, not to determine which documents are available. A URI need not be found in the **statically known documents** to be accessed using `fn:doc`.
- [Definition: **Statically known collections.** This is a mapping from strings to types. The string represents the absolute URI of a resource that is potentially available using the `fn:collection` function. The type is the type of the sequence of items that would result from calling the `fn:collection` function with this URI as its argument.] If the argument to `fn:collection` is a string literal that is not present in **statically known collections**, then the static type of `fn:collection` is `item()*`. **Note:** The purpose of the **statically known collections** is to provide static type information, not to determine which collections are available. A URI need not be found in the **statically known collections** to be accessed using `fn:collection`.
- [Definition: **Statically known default collection type.** This is the type of the sequence of items that would result from calling the `fn:collection` function with no arguments.] Unless initialized to some other value by an implementation, the value of **statically known default collection type** is `item()*`.
- [Definition: **Statically known decimal formats.** This is a mapping from QNames to decimal formats, with one default format that has no visible name, referred to as the unnamed decimal format. Each format is available for use when formatting numbers using the `fn:format-number` function.] Each decimal format defines a set of properties, which control the interpretation of characters in the picture string supplied to the `fn:format-number` function, and also specify characters to be used in the result of formatting the number. The following properties specify characters used both in the picture string, and in the formatted number. In each case the value is a single character: [Definition: **decimal-separator** is the character used to separate the integer part of the number from the fractional part, both in the picture string and in the formatted number; the default value is the period character (.)] [Definition: **exponent-separator** is the character used to separate the mantissa from the exponent in scientific notation both in the picture string and in the formatted number; the default value is the character (e).] [Definition: **grouping-separator** is the character typically used as a thousands separator, both in the picture string and in the formatted number; the default value is the comma character (,)] [Definition: **percent** is the character used both in the picture string and in the formatted number to indicate that the number is written as a per-hundred fraction; the default value is the percent character (%)] [Definition: **per-mille** is the character used both in the picture string and in the formatted number to indicate that the number is written as a per-thousand fraction; the default value is the Unicode per-mille character (#x2030)] [Definition: **zero-digit** is the character used to represent the digit zero; the default value is the Western digit zero (#x30). This character must be a digit (category Nd in the Unicode property database), and it must have the numeric value zero. This property implicitly defines the ten Unicode characters that are used to represent the values 0 to 9: Unicode is organized so that each set of decimal digits forms a contiguous block of characters in numerical sequence. Within the picture string any of these ten character can be used (interchangeably) as a place-holder for a mandatory digit. Within the final result string, these ten characters are used to represent the digits zero to nine.] The following properties specify characters to be used in the picture string supplied to the `fn:format-number` function, but not in the formatted number. In each case the value must be a single character. [Definition: **digit** is a character used in the picture string to represent an optional digit; the default value is the number sign character (#)] [Definition: **pattern-separator** is a character used to separate positive and negative sub-pictures in a picture string; the default value is the semi-colon character (;)] The following properties specify characters or strings that may appear in the result of formatting the number, but not in the picture string: [Definition: **infinity** is the string used to represent the double value infinity (`INF`); the default value is the string "Infinity"] [Definition: **NaN** is the string used to represent the double value NaN (not-a-number); the default value is the string "NaN"] [Definition: **minus-sign** is the single character used to mark negative numbers; the default value is the hyphen-minus character (#x2D). ]

#### 2.1.2 Dynamic Context

[Definition: The **dynamic context** of an expression is defined as information that is needed for the dynamic evaluation of an expression.] If evaluation of an expression relies on some part of the dynamic context that is [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31, a dynamic error is raised [err:XPDY0002].

The individual components of the dynamic context are described below. Further rules governing the semantics of these components can be found in **C.2 Dynamic Context Components**.

The dynamic context consists of all the components of the static context, and the additional components listed below.

[Definition: The first three components of the dynamic context (context item, context position, and context size) are called the **focus** of the expression. ] The focus enables the processor to keep track of which items are being processed by the expression. If any component in the focus is defined, both the context item and context position are known.

**Note:**

If any component in the focus is defined, context size is usually defined as well. However, when streaming, the context size cannot be determined without lookahead, so it may be undefined. If so, expressions like `last()` will raise a dynamic error because the context size is undefined.

[Definition: A **singleton focus** is a focus that refers to a single item; in a singleton focus, context item is set to the item, context position = 1 and context size = 1.]

Certain language constructs, notably the path operator `E1/E2`, the simple map operator `E1!E2`, and the predicate `E1[E2]`, create a new focus for the evaluation of a sub-expression. In these constructs, `E2` is evaluated once for each item in the sequence that results from evaluating `E1`. Each time `E2` is evaluated, it is evaluated with a different focus. The focus for evaluating `E2` is referred to below as the **inner focus**, while the focus for evaluating `E1` is referred to as the **outer focus**. The inner focus is used only for the evaluation of `E2`. Evaluation of E1 continues with its original focus unchanged.

- [Definition: The **context item** is the item currently being processed.] [Definition: When the context item is a node, it can also be referred to as the **context node**.] The context item is returned by an expression consisting of a single dot (`.`). When an expression `E1/E2` or `E1[E2]` is evaluated, each item in the sequence obtained by evaluating `E1` becomes the context item in the inner focus for an evaluation of `E2`.
- [Definition: The **context position** is the position of the context item within the sequence of items currently being processed.] It changes whenever the context item changes. When the focus is defined, the value of the context position is an integer greater than zero. The context position is returned by the expression `fn:position()`. When an expression `E1/E2` or `E1[E2]` is evaluated, the context position in the inner focus for an evaluation of `E2` is the position of the context item in the sequence obtained by evaluating `E1`. The position of the first item in a sequence is always 1 (one). The context position is always less than or equal to the context size.
- [Definition: The **context size** is the number of items in the sequence of items currently being processed.] Its value is always an integer greater than zero. The context size is returned by the expression `fn:last()`. When an expression `E1/E2` or `E1[E2]` is evaluated, the context size in the inner focus for an evaluation of `E2` is the number of items in the sequence obtained by evaluating `E1`.
- [Definition: **Variable values**. This is a mapping from expanded QName to value. It contains the same expanded QNames as the in-scope variables in the static context for the expression. The expanded QName is the name of the variable and the value is the dynamic value of the variable, which includes its dynamic type.]
- [Definition: **Named functions**. This is a mapping from (expanded QName, arity) to [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31. ] It supplies a function for each signature in statically known function signatures and may supply other functions (see **2.2.4 Consistency Constraints**). Named functions can include external functions. [Definition: **External functions** are functions that are implemented outside the query environment.] For example, an implementation might provide a set of implementation-defined external functions in addition to the core function library described in [XQuery and XPath Functions and Operators 3.1]. [Definition: An **implementation-defined function** is an external function that is implementation-defined ]. [Definition: A **host language function** is an external function defined by the host language.]
- [Definition: **Current dateTime.** This information represents an implementation-dependent point in time during the processing of an expression, and includes an explicit timezone. It can be retrieved by the `fn:current-dateTime` function. If invoked multiple times during the execution of an expression, this function always returns the same result.]
- [Definition: **Implicit timezone.** This is the timezone to be used when a date, time, or dateTime value that does not have a timezone is used in a comparison or arithmetic operation. The implicit timezone is an implementation-defined value of type `xs:dayTimeDuration`. See [Section 3.2.7.3 Timezones](https://www.w3.org/TR/xmlschema-2/#dateTime-timezones)XS1-2 or [Section 3.3.7 dateTime](https://www.w3.org/TR/xmlschema11-2/#dateTime)XS11-2 for the range of valid values of a timezone.]
- [Definition: **Default language.** This is the natural language used when creating human-readable output (for example, by the functions `fn:format-date` and `fn:format-integer`) if no other language is requested. The value is a language code as defined by the type `xs:language`.]
- [Definition: **Default calendar.** This is the calendar used when formatting dates in human-readable output (for example, by the functions `fn:format-date` and `fn:format-dateTime`) if no other calendar is requested. The value is a string.]
- [Definition: **Default place.** This is a geographical location used to identify the place where events happened (or will happen) when formatting dates and times using functions such as `fn:format-date` and `fn:format-dateTime`, if no other place is specified. It is used when translating timezone offsets to civil timezone names, and when using calendars where the translation from ISO dates/times to a local representation is dependent on geographical location. Possible representations of this information are an ISO country code or an Olson timezone name, but implementations are free to use other representations from which the above information can be derived.]
- [Definition: **Available documents.** This is a mapping of strings to document nodes. Each string represents the absolute URI of a resource. The document node is the root of a tree that represents that resource using the data model. The document node is returned by the `fn:doc` function when applied to that URI.] The set of available documents is not limited to the set of statically known documents, and it may be empty. If there are one or more URIs in available documents that map to a document node `D`, then the document-uri property of `D` must either be absent, or must be one of these URIs. **Note:** This means that given a document node `$N`, the result of `fn:doc(fn:document-uri($N)) is $N` will always be `true`, unless `fn:document-uri($N)` is an empty sequence.
- [Definition: **Available text resources**. This is a mapping of strings to text resources. Each string represents the absolute URI of a resource. The resource is returned by the `fn:unparsed-text` function when applied to that URI.] The set of available text resources is not limited to the set of statically known documents, and it may be empty.
- [Definition: **Available collections.** This is a mapping of strings to sequences of items. Each string represents the absolute URI of a resource. The sequence of items represents the result of the `fn:collection` function when that URI is supplied as the argument. ] The set of available collections is not limited to the set of statically known collections, and it may be empty. For every document node `D` that is in the target of a mapping in available collections, or that is the root of a tree containing such a node, the document-uri property of `D` must either be absent, or must be a URI `U` such that available documents contains a mapping from `U` to `D`. **Note:** This means that for any document node `$N` retrieved using the `fn:collection` function, either directly or by navigating to the root of a node that was returned, the result of `fn:doc(fn:document-uri($N)) is $N` will always be `true`, unless `fn:document-uri($N)` is an empty sequence. This implies a requirement for the `fn:doc` and `fn:collection` functions to be consistent in their effect. If the implementation uses catalogs or user-supplied URI resolvers to dereference URIs supplied to the `fn:doc` function, the implementation of the `fn:collection` function must take these mechanisms into account. For example, an implementation might achieve this by mapping the collection URI to a set of document URIs, which are then resolved using the same catalog or URI resolver that is used by the `fn:doc` function.
- [Definition: **Default collection.** This is the sequence of items that would result from calling the `fn:collection` function with no arguments.] The value of **default collection** may be initialized by the implementation.
- [Definition: **Available URI collections.** This is a mapping of strings to sequences of URIs. The string represents the absolute URI of a resource which can be interpreted as an aggregation of a number of individual resources each of which has its own URI. The sequence of URIs represents the result of the `fn:uri-collection` function when that URI is supplied as the argument. ] There is no implication that the URIs in this sequence can be successfully dereferenced, or that the resources they refer to have any particular media type. **Note:** An implementation **may** maintain some consistent relationship between the available collections and the available URI collections, for example by ensuring that the result of `fn:uri-collection(X)!fn:doc(.)` is the same as the result of `fn:collection(X)`. However, this is not required. The `fn:uri-collection` function is more general than `fn:collection` in that it allows access to resources other than XML documents; at the same time, `fn:collection` allows access to nodes that might lack individual URIs, for example nodes corresponding to XML fragments stored in the rows of a relational database.
- [Definition: **Default URI collection.** This is the sequence of URIs that would result from calling the `fn:uri-collection` function with no arguments.] The value of **default URI collection** may be initialized by the implementation.
- [Definition: **Environment variables.** This is a mapping from names to values. Both the names and the values are strings. The names are compared using an implementation-defined collation, and are unique under this collation. The set of environment variables is implementation-defined and **may** be empty.] **Note:** A possible implementation is to provide the set of POSIX environment variables (or their equivalent on other operating systems) appropriate to the process in which the expression is evaluated.

### 2.2 Processing Model

XPath 3.1 is defined in terms of the data model and the expression context.

Figure 1: Processing Model Overview

Figure 1 provides a schematic overview of the processing steps that are discussed in detail below. Some of these steps are completely outside the domain of XPath 3.1; in Figure 1, these are depicted outside the line that represents the boundaries of the language, an area labeled **external processing**. The external processing domain includes generation of XDM instances that represent the data to be queried (see **2.2.1 Data Model Generation**), schema import processing (see **2.2.2 Schema Import Processing**) and serialization. The area inside the boundaries of the language is known as the **XPath processing domain**, which includes the static analysis and dynamic evaluation phases (see **2.2.3 Expression Processing**). Consistency constraints on the XPath processing domain are defined in **2.2.4 Consistency Constraints**.

#### 2.2.1 Data Model Generation

The input data for an expression must be represented as one or more XDM instances. This process occurs outside the domain of XPath 3.1, which is why Figure 1 represents it in the external processing domain. Here are some steps by which an XML document might be converted to an XDM instance:

1. A document may be parsed using an XML parser that generates an **XML Information Set** (see [XML Infoset]). The parsed document may then be validated against one or more schemas. This process, which is described in [[XML Schema 1.0 Part 1]](https://www.w3.org/TR/xmlschema-1/) or [[XML Schema 1.1 Part 1]](https://www.w3.org/TR/xmlschema11-1/), results in an abstract information structure called the **Post-Schema Validation Infoset** (PSVI). If a document has no associated schema, its Information Set is preserved. (See DM1 in Fig. 1.)
2. The Information Set or PSVI may be transformed into an XDM instance by a process described in [XQuery and XPath Data Model (XDM) 3.1]. (See DM2 in Fig. 1.)

The above steps provide an example of how an XDM instance might be constructed. An XDM instance might also be synthesized directly from a relational database, or constructed in some other way (see DM3 in Fig. 1.) XPath 3.1 is defined in terms of the data model, but it does not place any constraints on how XDM instances are constructed.

[Definition: Each element node and attribute node in an XDM instance has a **type annotation** (described in [Section 2.7 Schema Information](https://www.w3.org/TR/xpath-datamodel-31/#types)DM31). The type annotation of a node is a reference to an XML Schema type. ] The `type-name` of a node is the name of the type referenced by its type annotation. If the XDM instance was derived from a validated XML document as described in [Section 3.3 Construction from a PSVI](https://www.w3.org/TR/xpath-datamodel-31/#const-psvi)DM31, the type annotations of the element and attribute nodes are derived from schema validation. XPath 3.1 does not provide a way to directly access the type annotation of an element or attribute node.

The value of an attribute is represented directly within the attribute node. An attribute node whose type is unknown (such as might occur in a schemaless document) is given the type annotation `xs:untypedAtomic`.

The value of an element is represented by the children of the element node, which may include text nodes and other element nodes. The type annotation of an element node indicates how the values in its child text nodes are to be interpreted. An element that has not been validated (such as might occur in a schemaless document) is annotated with the schema type `xs:untyped`. An element that has been validated and found to be partially valid is annotated with the schema type `xs:anyType`. If an element node is annotated as `xs:untyped`, all its descendant element nodes are also annotated as `xs:untyped`. However, if an element node is annotated as `xs:anyType`, some of its descendant element nodes may have a more specific type annotation.

#### 2.2.2 Schema Import Processing

The in-scope schema definitions in the static context are provided by the host language (see step SI1 in Figure 1) and must satisfy the consistency constraints defined in **2.2.4 Consistency Constraints**.

#### 2.2.3 Expression Processing

XPath 3.1 defines two phases of processing called the static analysis phase and the dynamic evaluation phase (see Fig. 1). During the static analysis phase, static errors, dynamic errors, or type errors may be raised. During the dynamic evaluation phase, only dynamic errors or type errors may be raised. These kinds of errors are defined in **2.3.1 Kinds of Errors**.

Within each phase, an implementation is free to use any strategy or algorithm whose result conforms to the specifications in this document.

##### 2.2.3.1 Static Analysis Phase

[Definition: The **static analysis phase** depends on the expression itself and on the static context. The **static analysis phase** does not depend on input data (other than schemas).]

During the static analysis phase, the XPath expression is parsed into an internal representation called the **operation tree** (step SQ1 in Figure 1). A parse error is raised as a static error [err:XPST0003]. The static context is initialized by the implementation (step SQ2). The static context is used to resolve schema type names, function names, namespace prefixes, and variable names (step SQ4). If a name of one of these kinds in the **operation tree** is not found in the static context, a static error ([err:XPST0008] or [err:XPST0017]) is raised (however, see exceptions to this rule in **2.5.5.3 Element Test** and **2.5.5.5 Attribute Test**.)

The **operation tree** is then **normalized** by making explicit the implicit operations such as atomization and extraction of Effective Boolean Values (step SQ5).

During the static analysis phase, a processor may perform type analysis. The effect of type analysis is to assign a static type to each expression in the operation tree. [Definition: The **static type** of an expression is the best inference that the processor is able to make statically about the type of the result of the expression.] This specification does not define the rules for type analysis nor the static types that are assigned to particular expressions: the only constraint is that the inferred type must match all possible values that the expression is capable of returning.

Examples of inferred static types might be:

- For the expression `concat(a,b)` the inferred static type is `xs:string`
- For the expression `$a = $v` the inferred static type is `xs:boolean`
- For the expression `$s[exp]` the inferred static type has the same item type as the static type of `$s`, but a cardinality that allows the empty sequence even if the static type of `$s` does not allow an empty sequence.
- The inferred static type of the expression `data($x)` (whether written explicitly or inserted into the operation tree in places where atomization is implicit) depends on the inferred static type of `$x`: for example, if `$x` has type `element(*, xs:integer)` then `data($x)` has static type `xs:integer`.

In XQuery 1.0 and XPath 2.0, rules for static type inferencing were published normatively in [XQuery 1.0 and XPath 2.0 Formal Semantics], but implementations were allowed to refine these rules to infer a more precise type where possible. In XQuery 3.1 and XPath 3.1, the rules for static type inferencing are entirely implementation-dependent.

Every kind of expression also imposes requirements on the type of its operands. For example, with the expression `substring($a, $b, $c)`, `$a` must be of type `xs:string` (or something that can be converted to `xs:string` by the function calling rules), while `$b` and `$c` must be of type `xs:double`.

If the Static Typing Feature is in effect, a processor must raise a type error during static analysis if the inferred static type of an expression is not subsumed by the required type of the context where the expression is used. For example, the call of substring above would cause a type error if the inferred static type of `$a` is `xs:integer`; equally, a type error would be reported during static analysis if the inferred static type is `xs:anyAtomicType`.

If the Static Typing Feature is not in effect, a processor may raise a type error during static analysis only if the inferred static type of an expression has no overlap (intersection) with the required type: so for the first argument of substring, the processor may raise an error if the inferred type is `xs:integer`, but not if it is `xs:anyAtomicType`. Alternatively, if the Static Typing Feature is not in effect, the processor may defer all type checking until the dynamic evaluation phase.

##### 2.2.3.2 Dynamic Evaluation Phase

[Definition: The **dynamic evaluation phase** is the phase during which the value of an expression is computed.] It is dependent on successful completion of the static analysis phase.

The dynamic evaluation phase can occur only if no errors were detected during the static analysis phase. If the Static Typing Feature is in effect, all type errors are detected during static analysis and serve to inhibit the dynamic evaluation phase.

The dynamic evaluation phase depends on the **operation tree** of the expression being evaluated (step DQ1), on the input data (step DQ4), and on the dynamic context (step DQ5), which in turn draws information from the external environment (step DQ3) and the static context (step DQ2). The dynamic evaluation phase may create new data-model values (step DQ4) and it may extend the dynamic context (step DQ5)—for example, by binding values to variables.

[Definition: A **dynamic type** is associated with each value as it is computed. The dynamic type of a value may be more specific than the static type of the expression that computed it (for example, the static type of an expression might be `xs:integer*`, denoting a sequence of zero or more integers, but at evaluation time its value may have the dynamic type `xs:integer`, denoting exactly one integer.)]

If an operand of an expression is found to have a dynamic type that is not appropriate for that operand, a type error is raised [err:XPTY0004].

Even though static typing can catch many type errors before an expression is executed, it is possible for an expression to raise an error during evaluation that was not detected by static analysis. For example, an expression may contain a cast of a string into an integer, which is statically valid. However, if the actual value of the string at run time cannot be cast into an integer, a dynamic error will result. Similarly, an expression may apply an arithmetic operator to a value whose static type is `xs:untypedAtomic`. This is not a static error, but at run time, if the value cannot be successfully cast to a numeric type, a dynamic error will be raised.

When the Static Typing Feature is in effect, it is also possible for static analysis of an expression to raise a type error, even though execution of the expression on certain inputs would be successful. For example, an expression might contain a function that requires an element as its parameter, and the static analysis phase might infer the static type of the function parameter to be an optional element. This case is treated as a type error and inhibits evaluation, even though the function call would have been successful for input data in which the optional element is present.

#### 2.2.4 Consistency Constraints

In order for XPath 3.1 to be well defined, the input XDM instances, the static context, and the dynamic context must be mutually consistent. The consistency constraints listed below are prerequisites for correct functioning of an XPath 3.1 implementation. Enforcement of these consistency constraints is beyond the scope of this specification. This specification does not define the result of an expression under any condition in which one or more of these constraints is not satisfied.

- For every node that has a type annotation, if that type annotation is found in the in-scope schema definitions (ISSD), then its definition in the ISSD must be equivalent to its definition in the type annotation.
- Every element name, attribute name, or schema type name referenced in in-scope variables or statically known function signatures must be in the in-scope schema definitions, unless it is an element name referenced as part of an ElementTest or an attribute name referenced as part of an AttributeTest.
- Any reference to a global element, attribute, or type name in the in-scope schema definitions must have a corresponding element, attribute or type definition in the in-scope schema definitions.
- For each mapping of a string to a document node in available documents, if there exists a mapping of the same string to a document type in statically known documents, the document node must match the document type, using the matching rules in **2.5.5 SequenceType Matching**.
- For each mapping of a string to a sequence of items in available collections, if there exists a mapping of the same string to a type in statically known collections, the sequence of items must match the type, using the matching rules in **2.5.5 SequenceType Matching**.
- The sequence of items in the default collection must match the statically known default collection type, using the matching rules in **2.5.5 SequenceType Matching**.
- The value of the context item must match the context item static type, using the matching rules in **2.5.5 SequenceType Matching**.
- For each (variable, type) pair in in-scope variables and the corresponding (variable, value) pair in variable values such that the variable names are equal, the value must match the type, using the matching rules in **2.5.5 SequenceType Matching**.
- In the statically known namespaces, the prefix `xml` must not be bound to any namespace URI other than `http://www.w3.org/XML/1998/namespace`, and no prefix other than `xml` may be bound to this namespace URI. The prefix `xmlns` must not be bound to any namespace URI, and no prefix may be bound to the namespace URI `http://www.w3.org/2000/xmlns/`.
- For each `(expanded QName, arity) -> FunctionTest` entry in statically known function signatures, there must exist an `(expanded QName, arity) -> function` entry in named functions such that the function's [signature](https://www.w3.org/TR/xpath-datamodel-31/#dt-signature)DM31 is `FunctionTest`.

### 2.3 Error Handling

#### 2.3.1 Kinds of Errors

As described in **2.2.3 Expression Processing**, XPath 3.1 defines a static analysis phase, which does not depend on input data, and a dynamic evaluation phase, which does depend on input data. Errors may be raised during each phase.

[Definition: An error that can be detected during the static analysis phase, and is not a type error, is a **static error**.] A syntax error is an example of a static error.

[Definition: A **dynamic error** is an error that must be detected during the dynamic evaluation phase and may be detected during the static analysis phase. Numeric overflow is an example of a dynamic error.]

[Definition: A **type error** may be raised during the static analysis phase or the dynamic evaluation phase. During the static analysis phase, a type error occurs when the static type of an expression does not match the expected type of the context in which the expression occurs. During the dynamic evaluation phase, a type error occurs when the dynamic type of a value does not match the expected type of the context in which the value occurs.]

The outcome of the static analysis phase is either success or one or more type errors, static errors, or statically-detected dynamic errors. The result of the dynamic evaluation phase is either a result value, a type error, or a dynamic error.

If more than one error is present, or if an error condition comes within the scope of more than one error defined in this specification, then any non-empty subset of these errors may be reported.

During the static analysis phase, if the Static Typing Feature is in effect and the static type assigned to an expression other than `()` or `data(())` is `empty-sequence()`, a static error is raised [err:XPST0005]. This catches cases in which a query refers to an element or attribute that is not present in the in-scope schema definitions, possibly because of a spelling error.

Independently of whether the Static Typing Feature is in effect, if an implementation can determine during the static analysis phase that an XPath expression, if evaluated, would necessarily raise a dynamic error or that an expression, if evaluated, would necessarily raise a type error, the implementation may (but is not required to) report that error during the static analysis phase.

An implementation can raise a dynamic error for an XPath expression statically only if the expression can never execute without raising that error, as in the following example:

```

error()
```

The following example contains a type error, which can be reported statically even if the implementation can not prove that the expression will actually be evaluated.

```

if (empty($arg))
then
  "cat" * 2
else
  0
```

[Definition: In addition to static errors, dynamic errors, and type errors, an XPath 3.1 implementation may raise **warnings**, either during the static analysis phase or the dynamic evaluation phase. The circumstances in which warnings are raised, and the ways in which warnings are handled, are implementation-defined.]

In addition to the errors defined in this specification, an implementation may raise a dynamic error for a reason beyond the scope of this specification. For example, limitations may exist on the maximum numbers or sizes of various objects. An error must be raised if such a limitation is exceeded [err:XPDY0130].

#### 2.3.2 Identifying and Reporting Errors

The errors defined in this specification are identified by QNames that have the form `err:XPYYnnnn`, where:

- `err` denotes the namespace for XPath and XQuery errors, `http://www.w3.org/2005/xqt-errors`. This binding of the namespace prefix `err` is used for convenience in this document, and is not normative.
- `XP` identifies the error as an XPath error (some errors, originally defined by XQuery and later added to XPath, use the code `XQ` instead).
- `YY` denotes the error category, using the following encoding: `ST` denotes a static error. `DY` denotes a dynamic error. `TY` denotes a type error.
- `nnnn` is a unique numeric code.

**Note:**

The namespace URI for XPath and XQuery errors is not expected to change from one version of XPath to another. However, the contents of this namespace may be extended to include additional error definitions.

The method by which an XPath 3.1 processor reports error information to the external environment is implementation-defined.

An error can be represented by a URI reference that is derived from the error QName as follows: an error with namespace URI *`NS`* and local part *`LP`* can be represented as the URI reference *`NS`* `#` *`LP`*. For example, an error whose QName is `err:XPST0017` could be represented as `http://www.w3.org/2005/xqt-errors#XPST0017`.

**Note:**

Along with a code identifying an error, implementations may wish to return additional information, such as the location of the error or the processing phase in which it was detected. If an implementation chooses to do so, then the mechanism that it uses to return this information is implementation-defined.

#### 2.3.3 Handling Dynamic Errors

Except as noted in this document, if any operand of an expression raises a dynamic error, the expression also raises a dynamic error. If an expression can validly return a value or raise a dynamic error, the implementation may choose to return the value or raise the dynamic error (see **2.3.4 Errors and Optimization**). For example, the logical expression `expr1 and expr2` may return the value `false` if either operand returns `false`, or may raise a dynamic error if either operand raises a dynamic error.

If more than one operand of an expression raises an error, the implementation may choose which error is raised by the expression. For example, in this expression:

```
($x div $y) + xs:decimal($z)
```

both the sub-expressions `($x div $y)` and `xs:decimal($z)` may raise an error. The implementation may choose which error is raised by the "`+`" expression. Once one operand raises an error, the implementation is not required, but is permitted, to evaluate any other operands.

[Definition: In addition to its identifying QName, a dynamic error may also carry a descriptive string and one or more additional values called **error values**.] An implementation may provide a mechanism whereby an application-defined error handler can process error values and produce diagnostic messages. The host language may also provide error handling mechanisms.

A dynamic error may be raised by a built-in function or operator. For example, the `div` operator raises an error if its operands are `xs:decimal` values and its second operand is equal to zero. Errors raised by built-in functions and operators are defined in [XQuery and XPath Functions and Operators 3.1].

A dynamic error can also be raised explicitly by calling the `fn:error` function, which always raises a dynamic error and never returns a value. This function is defined in [Section 3.1.1 fn:error](https://www.w3.org/TR/xpath-functions-31/#func-error)FO31. For example, the following function call raises a dynamic error, providing a QName that identifies the error, a descriptive string, and a diagnostic value (assuming that the prefix `app` is bound to a namespace containing application-defined error codes):

```
fn:error(xs:QName("app:err057"), "Unexpected value", fn:string($v))
```

#### 2.3.4 Errors and Optimization

Because different implementations may choose to evaluate or optimize an expression in different ways, certain aspects of raising dynamic errors are implementation-dependent, as described in this section.

An implementation is always free to evaluate the operands of an operator in any order.

In some cases, a processor can determine the result of an expression without accessing all the data that would be implied by the formal expression semantics. For example, the formal description of filter expressions suggests that `$s[1]` should be evaluated by examining all the items in sequence `$s`, and selecting all those that satisfy the predicate `position()=1`. In practice, many implementations will recognize that they can evaluate this expression by taking the first item in the sequence and then exiting. If `$s` is defined by an expression such as `//book[author eq 'Berners-Lee']`, then this strategy may avoid a complete scan of a large document and may therefore greatly improve performance. However, a consequence of this strategy is that a dynamic error or type error that would be detected if the expression semantics were followed literally might not be detected at all if the evaluation exits early. In this example, such an error might occur if there is a `book` element in the input data with more than one `author` subelement.

The extent to which a processor may optimize its access to data, at the cost of not raising errors, is defined by the following rules.

Consider an expression *Q* that has an operand (sub-expression) *E*. In general the value of *E* is a sequence. At an intermediate stage during evaluation of the sequence, some of its items will be known and others will be unknown. If, at such an intermediate stage of evaluation, a processor is able to establish that there are only two possible outcomes of evaluating *Q*, namely the value *V* or an error, then the processor may deliver the result *V* without evaluating further items in the operand *E*. For this purpose, two values are considered to represent the same outcome if their items are pairwise the same, where nodes are the same if they have the same identity, and values are the same if they are equal and have exactly the same type.

There is an exception to this rule: If a processor evaluates an operand *E* (wholly or in part), then it is required to establish that the actual value of the operand *E* does not violate any constraints on its cardinality. For example, the expression `$e eq 0` results in a type error if the value of `$e` contains two or more items. A processor is not allowed to decide, after evaluating the first item in the value of `$e` and finding it equal to zero, that the only possible outcomes are the value `true` or a type error caused by the cardinality violation. It must establish that the value of `$e` contains no more than one item.

These rules apply to all the operands of an expression considered in combination: thus if an expression has two operands *E1* and *E2*, it may be evaluated using any samples of the respective sequences that satisfy the above rules.

The rules cascade: if *A* is an operand of *B* and *B* is an operand of *C*, then the processor needs to evaluate only a sufficient sample of *B* to determine the value of *C*, and needs to evaluate only a sufficient sample of *A* to determine this sample of *B*.

The effect of these rules is that the processor is free to stop examining further items in a sequence as soon as it can establish that further items would not affect the result except possibly by causing an error. For example, the processor may return `true` as the result of the expression `S1 = S2` as soon as it finds a pair of equal values from the two sequences.

Another consequence of these rules is that where none of the items in a sequence contributes to the result of an expression, the processor is not obliged to evaluate any part of the sequence. Again, however, the processor cannot dispense with a required cardinality check: if an empty sequence is not permitted in the relevant context, then the processor must ensure that the operand is not an empty sequence.

Examples:

- If an implementation can find (for example, by using an index) that at least one item returned by `$expr1` in the following example has the value `47`, it is allowed to return `true` as the result of the `some` expression, without searching for another item returned by `$expr1` that would raise an error if it were evaluated. some $x in $expr1 satisfies $x = 47
- In the following example, if an implementation can find (for example, by using an index) the `product` element-nodes that have an `id` child with the value `47`, it is allowed to return these nodes as the result of the path expression, without searching for another `product` node that would raise an error because it has an `id` child whose value is not an integer. //product[id = 47]

For a variety of reasons, including optimization, implementations may rewrite expressions into a different form. There are a number of rules that limit the extent of this freedom:

- Other than the raising or not raising of errors, the result of evaluating a rewritten expression must conform to the semantics defined in this specification for the original expression. **Note:** This allows an implementation to return a result in cases where the original expression would have raised an error, or to raise an error in cases where the original expression would have returned a result. The main cases where this is likely to arise in practice are (a) where a rewrite changes the order of evaluation, such that a subexpression causing an error is evaluated when the expression is written one way and is not evaluated when the expression is written a different way, and (b) where intermediate results of the evaluation cause overflow or other out-of-range conditions. **Note:** This rule does not mean that the result of the expression will always be the same in non-error cases as if it had not been rewritten, because there are many cases where the result of an expression is to some degree implementation-dependent or implementation-defined.
- Conditional expressions must not raise a dynamic error in respect of subexpressions occurring in a branch that is not selected, and must not return the value delivered by a branch unless that branch is selected. Thus, the following example must not raise a dynamic error if the document `abc.xml` does not exist: if (doc-available('abc.xml')) then doc('abc.xml') else () Of course, the condition must be evaluated in order to determine which branch is selected, and the query must not be rewritten in a way that would bypass evaluating the condition.
- As stated earlier, an expression must not be rewritten to dispense with a required cardinality check: for example, `string-length(//title)` must raise an error if the document contains more than one title element.
- Expressions must not be rewritten in such a way as to create or remove static errors. The static errors in this specification are defined for the original expression, and must be preserved if the expression is rewritten.

Expression rewrite is illustrated by the following examples.

- Consider the expression `//part[color eq "Red"]`. An implementation might choose to rewrite this expression as `//part[color = "Red"][color eq "Red"]`. The implementation might then process the expression as follows: First process the "`=`" predicate by probing an index on parts by color to quickly find all the parts that have a Red color; then process the "`eq`" predicate by checking each of these parts to make sure it has only a single color. The result would be as follows: Parts that have exactly one color that is Red are returned. If some part has color Red together with some other color, an error is raised. The existence of some part that has no color Red but has multiple non-Red colors does not trigger an error.
- The expression in the following example cannot raise a casting error if it is evaluated exactly as written (i.e., left to right). Since neither predicate depends on the context position, an implementation might choose to reorder the predicates to achieve better performance (for example, by taking advantage of an index). This reordering could cause the expression to raise an error. $N[@x castable as xs:date][xs:date(@x) gt xs:date("2000-01-01")] To avoid unexpected errors caused by expression rewrite, tests that are designed to prevent dynamic errors should be expressed using conditional expressions. For example, the above expression can be written as follows: $N[if (@x castable as xs:date) then xs:date(@x) gt xs:date("2000-01-01") else false()]

### 2.4 Concepts

This section explains some concepts that are important to the processing of XPath 3.1 expressions.

#### 2.4.1 Document Order

An ordering called **document order** is defined among all the nodes accessible during processing of a given expression, which may consist of one or more **trees** (documents or fragments). Document order is defined in [Section 2.4 Document Order](https://www.w3.org/TR/xpath-datamodel-31/#document-order)DM31, and its definition is repeated here for convenience. Document order is a total ordering, although the relative order of some nodes is implementation-dependent. [Definition: Informally, **document order** is the order in which nodes appear in the XML serialization of a document.] [Definition: Document order is **stable**, which means that the relative order of two nodes will not change during the processing of a given expression, even if this order is implementation-dependent.] [Definition: The node ordering that is the reverse of document order is called **reverse document order**.]

Within a tree, document order satisfies the following constraints:

1. The root node is the first node.
2. Every node occurs before all of its children and descendants.
3. Namespace nodes immediately follow the element node with which they are associated. The relative order of namespace nodes is stable but implementation-dependent.
4. Attribute nodes immediately follow the namespace nodes of the element node with which they are associated. The relative order of attribute nodes is stable but implementation-dependent.
5. The relative order of siblings is the order in which they occur in the `children` property of their parent node.
6. Children and descendants occur before following siblings.

The relative order of nodes in distinct trees is stable but implementation-dependent, subject to the following constraint: If any node in a given tree T1 is before any node in a different tree T2, then all nodes in tree T1 are before all nodes in tree T2.

#### 2.4.2 Atomization

The semantics of some XPath 3.1 operators depend on a process called atomization. Atomization is applied to a value when the value is used in a context in which a sequence of atomic values is required. The result of atomization is either a sequence of atomic values or a type error [[err:FOTY0012](https://www.w3.org/TR/xpath-functions-31/#ERRFOTY0012)]FO31. [Definition: **Atomization** of a sequence is defined as the result of invoking the `fn:data` function, as defined in [Section 2.4 fn:data](https://www.w3.org/TR/xpath-functions-31/#func-data)FO31. ]

The semantics of `fn:data` are repeated here for convenience. The result of `fn:data` is the sequence of atomic values produced by applying the following rules to each item in the input sequence:

- If the item is an atomic value, it is returned.
- If the item is a node, its typed value is returned (a type error [[err:FOTY0012](https://www.w3.org/TR/xpath-functions-31/#ERRFOTY0012)]FO31 is raised if the node has no typed value.)
- If the item is a [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31 (other than an array) or map a type error [[err:FOTY0013](https://www.w3.org/TR/xpath-functions-31/#ERRFOTY0013)]FO31 is raised.
- If the item is an array `$a`, atomization is defined as `$a?* ! fn:data(.)`, which is equivalent to atomizing the members of the array. **Note:** This definition recursively atomizes members that are arrays. Hence, the result of atomizing the array `[ [1, 2, 3], [4, 5, 6] ]` is the sequence `(1, 2, 3, 4, 5, 6)`.

Atomization is used in processing the following types of expressions:

- Arithmetic expressions
- Comparison expressions
- Function calls and returns
- Cast expressions

#### 2.4.3 Effective Boolean Value

Under certain circumstances (listed below), it is necessary to find the effective boolean value of a value. [Definition: The **effective boolean value** of a value is defined as the result of applying the `fn:boolean` function to the value, as defined in [Section 7.3.1 fn:boolean](https://www.w3.org/TR/xpath-functions-31/#func-boolean)FO31.]

The dynamic semantics of `fn:boolean` are repeated here for convenience:

1. If its operand is an empty sequence, `fn:boolean` returns `false`.
2. If its operand is a sequence whose first item is a node, `fn:boolean` returns `true`.
3. If its operand is a singleton value of type `xs:boolean` or derived from `xs:boolean`, `fn:boolean` returns the value of its operand unchanged.
4. If its operand is a singleton value of type `xs:string`, `xs:anyURI`, `xs:untypedAtomic`, or a type derived from one of these, `fn:boolean` returns `false` if the operand value has zero length; otherwise it returns `true`.
5. If its operand is a singleton value of any numeric type or derived from a numeric type, `fn:boolean` returns `false` if the operand value is `NaN` or is numerically equal to zero; otherwise it returns `true`.
6. In all other cases, `fn:boolean` raises a type error [[err:FORG0006](https://www.w3.org/TR/xpath-functions-31/#ERRFORG0006)]FO31. **Note:** For instance, `fn:boolean` raises a type error if the operand is a function, a map, or an array.

The effective boolean value of a sequence is computed implicitly during processing of the following types of expressions:

- Logical expressions (`and`, `or`)
- The `fn:not` function
- Certain types of predicates, such as `a[b]`
- Conditional expressions (`if`)
- Quantified expressions (`some`, `every`)
- General comparisons, in XPath 1.0 compatibility mode.

**Note:**

The definition of effective boolean value is *not* used when casting a value to the type `xs:boolean`, for example in a `cast` expression or when passing a value to a function whose expected parameter is of type `xs:boolean`.

#### 2.4.4 Input Sources

XPath 3.1 has a set of functions that provide access to XML documents (`fn:doc`, `fn:doc-available`), collections (`fn:collection`, `fn:uri-collection`), text files (`fn:unparsed-text`, `fn:unparsed-text-lines`, `fn:unparsed-text-available`), and environment variables (`fn:environment-variable`, `fn:available-environment-variables`). These functions are defined in [Section 14.6 Functions giving access to external information](https://www.w3.org/TR/xpath-functions-31/#fns-on-docs)FO31.

An expression can access input data either by calling one of these input functions or by referencing some part of the dynamic context that is initialized by the external environment, such as a variable or context item.

#### 2.4.5 URI Literals

XPath 3.1 requires a statically known, valid URI in a BracedURILiteral. An implementation may raise a static error [err:XQST0046] if the value of a Braced URI Literal is of nonzero length and is neither an absolute URI nor a relative URI.

**Note:**

The `xs:anyURI` type is designed to anticipate the introduction of Internationalized Resource Identifiers (IRI's) as defined in [RFC3987].

Whitespace is normalized using the whitespace normalization rules of `fn:normalize-space`. If the result of whitespace normalization contains only whitespace, the corresponding URI consists of the empty string.

A Braced URI Literal or URI Literal is not subjected to percent-encoding or decoding as defined in [RFC3986].

#### 2.4.6 Resolving a Relative URI Reference

[Definition: To **resolve a relative URI** `$rel` against a base URI `$base` is to expand it to an absolute URI, as if by calling the function `fn:resolve-uri($rel, $base)`.] During static analysis, the base URI is the Static Base URI. During dynamic evaluation, the base URI used to resolve a relative URI reference depends on the semantics of the expression.

Any process that attempts to resolve URI against a base URI, or to dereference the URI, may apply percent-encoding or decoding as defined in the relevant RFCs.

### 2.5 Types

The type system of XPath 3.1 is based on [XML Schema 1.0] or [XML Schema 1.1].

[Definition: A **sequence type** is a type that can be expressed using the SequenceType syntax. Sequence types are used whenever it is necessary to refer to a type in an XPath 3.1 expression. The term **sequence type** suggests that this syntax is used to describe the type of an XPath 3.1 value, which is always a sequence.]

[Definition: A **schema type** is a type that is (or could be) defined using the facilities of [XML Schema 1.0] or [XML Schema 1.1] (including the built-in types).] A schema type can be used as a type annotation on an element or attribute node (unless it is a non-instantiable type such as `xs:NOTATION` or `xs:anyAtomicType`, in which case its derived types can be so used). Every schema type is either a **complex type** or a **simple type**; simple types are further subdivided into **list types**, **union types**, and **atomic types** (see [XML Schema 1.0] or [XML Schema 1.1] for definitions and explanations of these terms.)

[Definition: A **generalized atomic type** is a type which is either (a) an atomic type or (b) a pure union type ].

[Definition: A **pure union type** is an XML Schema union type that satisfies the following constraints: (1) `{variety}` is `union`, (2) the `{facets}` property is empty, (3) no type in the transitive membership of the union type has `{variety}` `list`, and (4) no type in the transitive membership of the union type is a type with `{variety}` `union` having a non-empty `{facets}` property].

**Note:**

The definition of pure union type excludes union types derived by non-trivial restriction from other union types, as well as union types that include list types in their membership. Pure union types have the property that every instance of an atomic type defined as one of the member types of the union is also a valid instance of the union type.

**Note:**

The current (second) edition of XML Schema 1.0 contains an error in respect of the substitutability of a union type by one of its members: it fails to recognize that this is unsafe if the union is derived by restriction from another union.

This problem is fixed in XSD 1.1, but the effect of the resolution is that an atomic value labeled with an atomic type cannot be treated as being substitutable for a union type without explicit validation. This specification therefore allows union types to be used as item types only if they are defined directly as the union of a number of atomic types.

Generalized atomic types represent the intersection between the categories of sequence type and schema type. A generalized atomic type, such as `xs:integer` or `my:hatsize`, is both a sequence type and a schema type.

#### 2.5.1 Predefined Schema Types

The in-scope schema types in the static context are initialized with a set of predefined schema types that is determined by the host language. This set may include some or all of the schema types in the namespace `http://www.w3.org/2001/XMLSchema`, represented in this document by the namespace prefix `xs`. The schema types in this namespace are defined in [XML Schema 1.0] or [XML Schema 1.1] and augmented by additional types defined in [XQuery and XPath Data Model (XDM) 3.1]. An implementation that has based its type system on [XML Schema 1.0] is not required to support the `xs:dateTimeStamp` or `xs:error` types.

The schema types defined in [Section 2.7.2 Predefined Types](https://www.w3.org/TR/xpath-datamodel-31/#types-predefined)DM31 are summarized below.

1. [Definition: `xs:untyped` is used as the type annotation of an element node that has not been validated, or has been validated in `skip` mode.] No predefined schema types are derived from `xs:untyped`.
2. [Definition: `xs:untypedAtomic` is an atomic type that is used to denote untyped atomic data, such as text that has not been assigned a more specific type.] An attribute that has been validated in `skip` mode is represented in the data model by an attribute node with the type annotation `xs:untypedAtomic`. No predefined schema types are derived from `xs:untypedAtomic`.
3. [Definition: `xs:dayTimeDuration` is derived by restriction from `xs:duration`. The lexical representation of `xs:dayTimeDuration` is restricted to contain only day, hour, minute, and second components.]
4. [Definition: `xs:yearMonthDuration` is derived by restriction from `xs:duration`. The lexical representation of `xs:yearMonthDuration` is restricted to contain only year and month components.]
5. [Definition: `xs:anyAtomicType` is an atomic type that includes all atomic values (and no values that are not atomic). Its base type is `xs:anySimpleType` from which all simple types, including atomic, list, and union types, are derived. All primitive atomic types, such as `xs:decimal` and `xs:string`, have `xs:anyAtomicType` as their base type.] **Note:** `xs:anyAtomicType` will not appear as the type of an actual value in an XDM instance.
6. [Definition: `xs:error` is a simple type with no value space. It is defined in [Section 3.16.7.3 xs:error](https://www.w3.org/TR/xmlschema11-1/#xsd-error)XS11-1 and can be used in the **2.5.4 SequenceType Syntax** to raise errors.]

The relationships among the schema types in the `xs` namespace are illustrated in Figure 2. A more complete description of the XPath 3.1 type hierarchy can be found in [Section 1.6 Type System](https://www.w3.org/TR/xpath-functions-31/#datatypes)FO31.

Figure 2: Hierarchy of Schema Types used in XPath 3.1.

#### 2.5.2 Namespace-sensitive Types

[Definition: The **namespace-sensitive** types are `xs:QName`, `xs:NOTATION`, types derived by restriction from `xs:QName` or `xs:NOTATION`, list types that have a namespace-sensitive item type, and union types with a namespace-sensitive type in their transitive membership.]

It is not possible to preserve the type of a namespace-sensitive value without also preserving the namespace binding that defines the meaning of each namespace prefix used in the value. Therefore, XPath 3.1 defines some error conditions that occur only with namespace-sensitive values. For instance, casting to a namespace-sensitive type raises a type error [[err:FONS0004](https://www.w3.org/TR/xpath-functions-31/#ERRFONS0004)]FO31 if the namespace bindings for the result cannot be determined.

#### 2.5.3 Typed Value and String Value

Every node has a **typed value** and a **string value**, except for nodes whose value is [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31. [Definition: The **typed value** of a node is a sequence of atomic values and can be extracted by applying the [Section 2.4 fn:data](https://www.w3.org/TR/xpath-functions-31/#func-data)FO31 function to the node.] [Definition: The **string value** of a node is a string and can be extracted by applying the [Section 2.3 fn:string](https://www.w3.org/TR/xpath-functions-31/#func-string)FO31 function to the node.]

An implementation may store both the typed value and the string value of a node, or it may store only one of these and derive the other as needed. The string value of a node must be a valid lexical representation of the typed value of the node, but the node is not required to preserve the string representation from the original source document. For example, if the typed value of a node is the `xs:integer` value `30`, its string value might be "`30`" or "`0030`".

The typed value, string value, and type annotation of a node are closely related. If the node was created by mapping from an Infoset or PSVI, the relationships among these properties are defined by rules in [Section 2.7 Schema Information](https://www.w3.org/TR/xpath-datamodel-31/#types)DM31.

As a convenience to the reader, the relationship between typed value and string value for various kinds of nodes is summarized and illustrated by examples below.

1. For text and document nodes, the typed value of the node is the same as its string value, as an instance of the type `xs:untypedAtomic`. The string value of a document node is formed by concatenating the string values of all its descendant text nodes, in document order.
2. The typed value of a comment, namespace, or processing instruction node is the same as its string value. It is an instance of the type `xs:string`.
3. The typed value of an attribute node with the type annotation `xs:anySimpleType` or `xs:untypedAtomic` is the same as its string value, as an instance of `xs:untypedAtomic`. The typed value of an attribute node with any other type annotation is derived from its string value and type annotation using the lexical-to-value-space mapping defined in [XML Schema 1.0] or [XML Schema 1.1] Part 2 for the relevant type. Example: A1 is an attribute having string value `"3.14E-2"` and type annotation `xs:double`. The typed value of A1 is the `xs:double` value whose lexical representation is `3.14E-2`. Example: A2 is an attribute with type annotation `xs:IDREFS`, which is a list datatype whose item type is the atomic datatype `xs:IDREF`. Its string value is "`bar baz faz`". The typed value of A2 is a sequence of three atomic values ("`bar`", "`baz`", "`faz`"), each of type `xs:IDREF`. The typed value of a node is never treated as an instance of a named list type. Instead, if the type annotation of a node is a list type (such as `xs:IDREFS`), its typed value is treated as a sequence of the generalized atomic type from which it is derived (such as `xs:IDREF`).
4. For an element node, the relationship between typed value and string value depends on the node's type annotation, as follows: If the type annotation is `xs:untyped` or `xs:anySimpleType` or denotes a complex type with mixed content (including `xs:anyType`), then the typed value of the node is equal to its string value, as an instance of `xs:untypedAtomic`. However, if the `nilled` property of the node is `true`, then its typed value is the empty sequence. Example: E1 is an element node having type annotation `xs:untyped` and string value "`1999-05-31`". The typed value of E1 is "`1999-05-31`", as an instance of `xs:untypedAtomic`. Example: E2 is an element node with the type annotation `formula`, which is a complex type with mixed content. The content of E2 consists of the character "`H`", a child element named `subscript` with string value "`2`", and the character "`O`". The typed value of E2 is "`H2O`" as an instance of `xs:untypedAtomic`. If the type annotation denotes a simple type or a complex type with simple content, then the typed value of the node is derived from its string value and its type annotation in a way that is consistent with schema validation. However, if the `nilled` property of the node is `true`, then its typed value is the empty sequence. Example: E3 is an element node with the type annotation `cost`, which is a complex type that has several attributes and a simple content type of `xs:decimal`. The string value of E3 is "`74.95`". The typed value of E3 is `74.95`, as an instance of `xs:decimal`. Example: E4 is an element node with the type annotation `hatsizelist`, which is a simple type derived from the atomic type `hatsize`, which in turn is derived from `xs:integer`. The string value of E4 is "`7 8 9`". The typed value of E4 is a sequence of three values (`7`, `8`, `9`), each of type `hatsize`. Example: E5 is an element node with the type annotation `my:integer-or-string` which is a union type with member types `xs:integer` and `xs:string`. The string value of E5 is "`47`". The typed value of E5 is `47` as an `xs:integer`, since `xs:integer` is the member type that validated the content of E5. In general, when the type annotation of a node is a union type, the typed value of the node will be an instance of one of the member types of the union. **Note:** If an implementation stores only the string value of a node, and the type annotation of the node is a union type, the implementation must be able to deliver the typed value of the node as an instance of the appropriate member type. If the type annotation denotes a complex type with empty content, then the typed value of the node is the empty sequence and its string value is the zero-length string. If the type annotation denotes a complex type with element-only content, then the typed value of the node is [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31. The `fn:data` function raises a type error [[err:FOTY0012](https://www.w3.org/TR/xpath-functions-31/#ERRFOTY0012)]FO31 when applied to such a node. The string value of such a node is equal to the concatenated string values of all its text node descendants, in document order. Example: E6 is an element node with the type annotation `weather`, which is a complex type whose content type specifies `element-only`. E6 has two child elements named `temperature` and `precipitation`. The typed value of E6 is [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31, and the `fn:data` function applied to E6 raises an error.

#### 2.5.4 SequenceType Syntax

Whenever it is necessary to refer to a type in an XPath 3.1 expression, the SequenceType syntax is used.

| [79]                                                                             | `SequenceType`                                                                   | ::=                                                                              | `("empty-sequence" "(" ")")\| (ItemType OccurrenceIndicator?)`                   |                                                                                  |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [81]                                                                             | `ItemType`                                                                       | ::=                                                                              | ` KindTest \| ("item" "(" ")") \| FunctionTest \| MapTest \| ArrayTest \| Atomic |                                                                                  |
| [80]                                                                             | `OccurrenceIndicator`                                                            | ::=                                                                              | `"?" \| "*" \| "+"`                                                              | */* xgc: occurrence-indicators */*                                               |
| [82]                                                                             | `AtomicOrUnionType`                                                              | ::=                                                                              | ` EQName `                                                                       |                                                                                  |
| [83]                                                                             | `KindTest`                                                                       | ::=                                                                              | ` DocumentTest \| ElementTest \| AttributeTest \| SchemaElementTest \| SchemaAtt |                                                                                  |
| [85]                                                                             | `DocumentTest`                                                                   | ::=                                                                              | `"document-node" "(" (ElementTest \| SchemaElementTest)? ")"`                    |                                                                                  |
| [94]                                                                             | `ElementTest`                                                                    | ::=                                                                              | `"element" "(" (ElementNameOrWildcard ("," TypeName "?"?)?)? ")"`                |                                                                                  |
| [96]                                                                             | `SchemaElementTest`                                                              | ::=                                                                              | `"schema-element" "(" ElementDeclaration ")"`                                    |                                                                                  |
| [97]                                                                             | `ElementDeclaration`                                                             | ::=                                                                              | ` ElementName `                                                                  |                                                                                  |
| [90]                                                                             | `AttributeTest`                                                                  | ::=                                                                              | `"attribute" "(" (AttribNameOrWildcard ("," TypeName)?)? ")"`                    |                                                                                  |
| [92]                                                                             | `SchemaAttributeTest`                                                            | ::=                                                                              | `"schema-attribute" "(" AttributeDeclaration ")"`                                |                                                                                  |
| [93]                                                                             | `AttributeDeclaration`                                                           | ::=                                                                              | ` AttributeName `                                                                |                                                                                  |
| [95]                                                                             | `ElementNameOrWildcard`                                                          | ::=                                                                              | ` ElementName \| "*"`                                                            |                                                                                  |
| [99]                                                                             | `ElementName`                                                                    | ::=                                                                              | ` EQName `                                                                       |                                                                                  |
| [91]                                                                             | `AttribNameOrWildcard`                                                           | ::=                                                                              | ` AttributeName \| "*"`                                                          |                                                                                  |
| [98]                                                                             | `AttributeName`                                                                  | ::=                                                                              | ` EQName `                                                                       |                                                                                  |
| [101]                                                                            | `TypeName`                                                                       | ::=                                                                              | ` EQName `                                                                       |                                                                                  |
| [89]                                                                             | `PITest`                                                                         | ::=                                                                              | `"processing-instruction" "(" (NCName \| StringLiteral)? ")"`                    |                                                                                  |
| [87]                                                                             | `CommentTest`                                                                    | ::=                                                                              | `"comment" "(" ")"`                                                              |                                                                                  |
| [88]                                                                             | `NamespaceNodeTest`                                                              | ::=                                                                              | `"namespace-node" "(" ")"`                                                       |                                                                                  |
| [86]                                                                             | `TextTest`                                                                       | ::=                                                                              | `"text" "(" ")"`                                                                 |                                                                                  |
| [84]                                                                             | `AnyKindTest`                                                                    | ::=                                                                              | `"node" "(" ")"`                                                                 |                                                                                  |
| [102]                                                                            | `FunctionTest`                                                                   | ::=                                                                              | ` AnyFunctionTest \| TypedFunctionTest `                                         |                                                                                  |
| [103]                                                                            | `AnyFunctionTest`                                                                | ::=                                                                              | `"function" "(" "*" ")"`                                                         |                                                                                  |
| [104]                                                                            | `TypedFunctionTest`                                                              | ::=                                                                              | `"function" "(" (SequenceType ("," SequenceType)*)? ")" "as" SequenceType `      |                                                                                  |
| [111]                                                                            | `ParenthesizedItemType`                                                          | ::=                                                                              | `"(" ItemType ")"`                                                               |                                                                                  |
| [105]                                                                            | `MapTest`                                                                        | ::=                                                                              | ` AnyMapTest \| TypedMapTest `                                                   |                                                                                  |
| [108]                                                                            | `ArrayTest`                                                                      | ::=                                                                              | ` AnyArrayTest \| TypedArrayTest `                                               |                                                                                  |

With the exception of the special type `empty-sequence()`, a sequence type consists of an **item type** that constrains the type of each item in the sequence, and a **cardinality** that constrains the number of items in the sequence. Apart from the item type `item()`, which permits any kind of item, item types divide into **node types** (such as `element()`), **generalized atomic types** (such as `xs:integer`) and function types (such as function() as item()*).

Lexical QNames appearing in a sequence type have their prefixes expanded to namespace URIs by means of the statically known namespaces and (where applicable) the default element/type namespace. Equality of QNames is defined by the `eq` operator.

Item types representing element and attribute nodes may specify the required type annotations of those nodes, in the form of a schema type. Thus the item type `element(*, us:address)` denotes any element node whose type annotation is (or is derived from) the schema type named `us:address`.

The occurrence indicators '+', '*', and '?' bind to the last ItemType in the SequenceType, as described in occurrence-indicators constraint.

Here are some examples of sequence types that might be used in XPath 3.1:

- `xs:date` refers to the built-in atomic schema type named `xs:date`
- `attribute()?` refers to an optional attribute node
- `element()` refers to any element node
- `element(po:shipto, po:address)` refers to an element node that has the name `po:shipto` and has the type annotation `po:address` (or a schema type derived from `po:address`)
- `element(*, po:address)` refers to an element node of any name that has the type annotation `po:address` (or a type derived from `po:address`)
- `element(customer)` refers to an element node named `customer` with any type annotation
- `schema-element(customer)` refers to an element node whose name is `customer` (or is in the substitution group headed by `customer`) and whose type annotation matches the schema type declared for a `customer` element in the in-scope element declarations
- `node()*` refers to a sequence of zero or more nodes of any kind
- `item()+` refers to a sequence of one or more items
- `function(*)` refers to any [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31, regardless of arity or type
- `function(node()) as xs:string*` refers to a [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31 that takes a single argument whose value is a single node, and returns a sequence of zero or more xs:string values
- `(function(node()) as xs:string)*` refers to a sequence of zero or more [functions](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31, each of which takes a single argument whose value is a single node, and returns as its result a single xs:string value

#### 2.5.5 SequenceType Matching

[Definition: **SequenceType matching** compares the dynamic type of a value with an expected sequence type. ] For example, an `instance of` expression returns `true` if the dynamic type of a given value matches a given sequence type, or `false` if it does not.

An XPath 3.1 implementation must be able to determine relationships among the types in type annotations in an XDM instance and the types in the in-scope schema definitions (ISSD).

[Definition: The use of a value whose dynamic type is derived from an expected type is known as **subtype substitution**.] Subtype substitution does not change the actual type of a value. For example, if an `xs:integer` value is used where an `xs:decimal` value is expected, the value retains its type as `xs:integer`.

The definition of SequenceType matching relies on a pseudo-function named `derives-from(` *AT*, *ET* `)`, which takes an actual simple or complex schema type *AT* and an expected simple or complex schema type *ET*, and either returns a boolean value or raises a type error [err:XPTY0004]. This function is defined as follows:

- `derives-from(` *AT*, *ET* `)` raises a type error [err:XPTY0004] if *ET* is not present in the in-scope schema definitions (ISSD).
- `derives-from(` *AT*, *ET* `)` returns `true` if any of the following conditions applies: *AT* is *ET* *ET* is the base type of *AT* *ET* is a pure union type of which *AT* is a member type There is a type *MT* such that `derives-from(` *AT*, *MT* `)` and `derives-from(` *MT*, *ET* `)`
- Otherwise, `derives-from(` *AT*, *ET* `)` returns `false`

The rules for SequenceType matching are given below, with examples (the examples are for purposes of illustration, and do not cover all possible cases).

##### 2.5.5.1 Matching a SequenceType and a Value

- The sequence type `empty-sequence()` matches a value that is the empty sequence.
- An ItemType with no OccurrenceIndicator matches any value that contains exactly one item if the ItemType matches that item (see **2.5.5.2 Matching an ItemType and an Item**).
- An ItemType with an OccurrenceIndicator matches a value if the number of items in the value matches the OccurrenceIndicator and the ItemType matches each of the items in the value.

An OccurrenceIndicator specifies the number of items in a sequence, as follows:

- `?` matches zero or one items
- `*` matches zero or more items
- `+` matches one or more items

As a consequence of these rules, any sequence type whose OccurrenceIndicator is `*` or `?` matches a value that is an empty sequence.

##### 2.5.5.2 Matching an ItemType and an Item

- An ItemType consisting simply of an EQName is interpreted as an AtomicOrUnionType. The expected type *AtomicOrUnionType* matches an atomic value whose actual type is *AT* if `derives-from(` *AT, AtomicOrUnionType* `)` is `true`. The name of an AtomicOrUnionType has its prefix expanded to a namespace URI by means of the statically known namespaces, or if unprefixed, the default element/type namespace. If the expanded QName of an AtomicOrUnionType is not defined as a generalized atomic type in the in-scope schema types, a static error is raised [err:XPST0051]. Example: The ItemType `xs:decimal` matches any value of type `xs:decimal`. It also matches any value of type `shoesize`, if `shoesize` is an atomic type derived by restriction from `xs:decimal`. Example: Suppose ItemType `dress-size` is a union type that allows either `xs:decimal` values for numeric sizes (e.g. 4, 6, 10, 12), or one of an enumerated set of `xs:strings` (e.g. "small", "medium", "large"). The ItemType `dress-size` matches any of these values. **Note:** The names of non-atomic types such as `xs:IDREFS` are not accepted in this context, but can often be replaced by a generalized atomic type with an occurrence indicator, such as `xs:IDREF+`.
- `item()` matches any single item. Example: `item()` matches the atomic value `1`, the element `<a/>`, or the function `fn:concat#3`.
- `node()` matches any node.
- `text()` matches any text node.
- `processing-instruction()` matches any processing-instruction node.
- `processing-instruction(` *N* `)` matches any processing-instruction node whose PITarget is equal to `fn:normalize-space(N)`. If `fn:normalize-space(N)` is not in the lexical space of NCName, a type error is raised [err:XPTY0004] Example: `processing-instruction(xml-stylesheet)` matches any processing instruction whose PITarget is `xml-stylesheet`. For backward compatibility with XPath 1.0, the PITarget of a processing instruction may also be expressed as a string literal, as in this example: `processing-instruction("xml-stylesheet")`. If the specified PITarget is not a syntactically valid NCName, a type error is raised [err:XPTY0004].
- `comment()` matches any comment node.
- `namespace-node()` matches any namespace node.
- `document-node()` matches any document node.
- `document-node(` *E* `)` matches any document node that contains exactly one element node, optionally accompanied by one or more comment and processing instruction nodes, if *E* is an ElementTest or SchemaElementTest that matches the element node (see **2.5.5.3 Element Test** and **2.5.5.4 Schema Element Test**). Example: `document-node(element(book))` matches a document node containing exactly one element node that is matched by the ElementTest `element(book)`.
- A ParenthesizedItemType matches an item if and only if the item matches the ItemType that is in parentheses.
- An ItemType that is an ElementTest, SchemaElementTest, AttributeTest, SchemaAttributeTest, or FunctionTest matches an item as described in the following sections.
- The `ItemType` `map(K, V)` matches an item M if (a) M is a map, and (b) every entry in M has a key that matches `K` and an associated value that matches `V`. For example, `map(xs:integer, element(employee))` matches a map if all the keys in the map are integers, and all the associated values are `employee` elements. Note that a map (like a sequence) carries no intrinsic type information separate from the types of its entries, and the type of existing entries in a map does not constrain the type of new entries that can be added to the map. **Note:** In consequence, `map(K, V)` matches an empty map, whatever the types K and V might be.
- The `ItemType` `map(*)` matches any map regardless of its contents. It is equivalent to `map(xs:anyAtomicType, item()*)`.
- The `ItemType` `array(T)` matches any array in which the type of every member is `T`.
- The `ItemType` `array(*)` matches any array regardless of its contents.

##### 2.5.5.3 Element Test

| [94]                                                              | `ElementTest`                                                     | ::=                                                               | `"element" "(" (ElementNameOrWildcard ("," TypeName "?"?)?)? ")"` |                                                                   |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| [95]                                                              | `ElementNameOrWildcard`                                           | ::=                                                               | ` ElementName \| "*"`                                             |                                                                   |
| [99]                                                              | `ElementName`                                                     | ::=                                                               | ` EQName `                                                        |                                                                   |
| [101]                                                             | `TypeName`                                                        | ::=                                                               | ` EQName `                                                        |                                                                   |

An ElementTest is used to match an element node by its name and/or type annotation.

The ElementName and TypeName of an ElementTest have their prefixes expanded to namespace URIs by means of the statically known namespaces, or if unprefixed, the default element/type namespace. The ElementName need not be present in the in-scope element declarations, but the TypeName must be present in the in-scope schema types [err:XPST0008]. Note that substitution groups do not affect the semantics of ElementTest.

An ElementTest may take any of the following forms:

1. `element()` and `element(*)` match any single element node, regardless of its name or type annotation.
2. `element(` ElementName `)` matches any element node whose name is ElementName, regardless of its type annotation or `nilled` property. Example: `element(person)` matches any element node whose name is `person`.
3. `element(` ElementName `,` TypeName `)` matches an element node whose name is ElementName if `derives-from(` *AT*, TypeName `)` is `true`, where *AT* is the type annotation of the element node, and the `nilled` property of the node is `false`. Example: `element(person, surgeon)` matches a non-nilled element node whose name is `person` and whose type annotation is `surgeon` (or is derived from `surgeon`).
4. `element(` ElementName, TypeName ` ?)` matches an element node whose name is ElementName if `derives-from(` *AT*, TypeName `)` is `true`, where *AT* is the type annotation of the element node. The `nilled` property of the node may be either `true` or `false`. Example: `element(person, surgeon?)` matches a nilled or non-nilled element node whose name is `person` and whose type annotation is `surgeon` (or is derived from `surgeon`).
5. `element(*, ` TypeName `)` matches an element node regardless of its name, if `derives-from(` *AT*, TypeName `)` is `true`, where *AT* is the type annotation of the element node, and the `nilled` property of the node is `false`. Example: `element(*, surgeon)` matches any non-nilled element node whose type annotation is `surgeon` (or is derived from `surgeon`), regardless of its name.
6. `element(*,` TypeName ` ?)` matches an element node regardless of its name, if `derives-from(` *AT*, TypeName `)` is `true`, where *AT* is the type annotation of the element node. The `nilled` property of the node may be either `true` or `false`. Example: `element(*, surgeon?)` matches any nilled or non-nilled element node whose type annotation is `surgeon` (or is derived from `surgeon`), regardless of its name.

##### 2.5.5.4 Schema Element Test

| [96]                                          | `SchemaElementTest`                           | ::=                                           | `"schema-element" "(" ElementDeclaration ")"` |                                               |
| --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- |
| [97]                                          | `ElementDeclaration`                          | ::=                                           | ` ElementName `                               |                                               |
| [99]                                          | `ElementName`                                 | ::=                                           | ` EQName `                                    |                                               |

A SchemaElementTest matches an element node against a corresponding element declaration found in the in-scope element declarations.

The ElementName of a SchemaElementTest has its prefixes expanded to a namespace URI by means of the statically known namespaces, or if unprefixed, the default element/type namespace. If the ElementName specified in the SchemaElementTest is not found in the in-scope element declarations, a static error is raised [err:XPST0008].

A SchemaElementTest matches a candidate element node if all of the following conditions are satisfied:

1. Either: The name *N* of the candidate node matches the specified ElementName, or The name *N* of the candidate node matches the name of an element declaration that is a member of the actual substitution group headed by the declaration of element ElementName. **Note:** The term "actual substitution group" is defined in [XML Schema 1.1]. The actual substitution group of an element declaration *H* includes those element declarations *P* that are declared to have *H* as their direct or indirect substitution group head, provided that *P* is not declared as abstract, and that *P* is validly substitutable for *H*, which means that there must be no blocking constraints that prevent substitution.
2. The schema element declaration named *N* is not abstract.
3. `derives-from( AT, ET )` is true, where *AT* is the type annotation of the candidate node and *ET* is the schema type declared in the schema element declaration named *N*.
4. If the schema element declaration named *N* is not nillable, then the nilled property of the candidate node is false.

Example: The SchemaElementTest `schema-element(customer)` matches a candidate element node in the following two situations:

1. customer is a top-level element declaration in the in-scope element declarations; the name of the candidate node is customer; the element declaration of customer is not abstract; the type annotation of the candidate node is the same as or derived from the schema type declared in the customer element declaration; and either the candidate node is not nilled, or customer is declared to be nillable.
2. customer is a top-level element declaration in the in-scope element declarations; the name of the candidate node is client; client is an actual (non-abstract and non-blocked) member of the substitution group of customer; the type annotation of the candidate node is the same as or derived from the schema type declared for the client element; and either the candidate node is not nilled, or client is declared to be nillable.

##### 2.5.5.5 Attribute Test

| [90]                                                          | `AttributeTest`                                               | ::=                                                           | `"attribute" "(" (AttribNameOrWildcard ("," TypeName)?)? ")"` |                                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| [91]                                                          | `AttribNameOrWildcard`                                        | ::=                                                           | ` AttributeName \| "*"`                                       |                                                               |
| [98]                                                          | `AttributeName`                                               | ::=                                                           | ` EQName `                                                    |                                                               |
| [101]                                                         | `TypeName`                                                    | ::=                                                           | ` EQName `                                                    |                                                               |

An AttributeTest is used to match an attribute node by its name and/or type annotation.

The AttributeName and TypeName of an AttributeTest have their prefixes expanded to namespace URIs by means of the statically known namespaces. If unprefixed, the AttributeName is in no namespace, but an unprefixed TypeName is in the default element/type namespace. The AttributeName need not be present in the in-scope attribute declarations, but the TypeName must be present in the in-scope schema types [err:XPST0008].

An AttributeTest may take any of the following forms:

1. `attribute()` and `attribute(*)` match any single attribute node, regardless of its name or type annotation.
2. `attribute(` AttributeName `)` matches any attribute node whose name is AttributeName, regardless of its type annotation. Example: `attribute(price)` matches any attribute node whose name is `price`.
3. `attribute(` AttributeName, TypeName `)` matches an attribute node whose name is AttributeName if `derives-from(` *AT*, TypeName `)` is `true`, where *AT* is the type annotation of the attribute node. Example: `attribute(price, currency)` matches an attribute node whose name is `price` and whose type annotation is `currency` (or is derived from `currency`).
4. `attribute(*, ` TypeName `)` matches an attribute node regardless of its name, if `derives-from(` *AT*, TypeName `)` is `true`, where *AT* is the type annotation of the attribute node. Example: `attribute(*, currency)` matches any attribute node whose type annotation is `currency` (or is derived from `currency`), regardless of its name.

##### 2.5.5.6 Schema Attribute Test

| [92]                                              | `SchemaAttributeTest`                             | ::=                                               | `"schema-attribute" "(" AttributeDeclaration ")"` |                                                   |
| ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| [93]                                              | `AttributeDeclaration`                            | ::=                                               | ` AttributeName `                                 |                                                   |
| [98]                                              | `AttributeName`                                   | ::=                                               | ` EQName `                                        |                                                   |

A SchemaAttributeTest matches an attribute node against a corresponding attribute declaration found in the in-scope attribute declarations.

The AttributeName of a SchemaAttributeTest has its prefixes expanded to a namespace URI by means of the statically known namespaces. If unprefixed, an AttributeName is in no namespace. If the AttributeName specified in the SchemaAttributeTest is not found in the in-scope attribute declarations, a static error is raised [err:XPST0008].

A SchemaAttributeTest matches a candidate attribute node if both of the following conditions are satisfied:

1. The name of the candidate node matches the specified AttributeName.
2. `derives-from(` *AT, ET* `)` is `true`, where *AT* is the type annotation of the candidate node and *ET* is the schema type declared for attribute AttributeName in the in-scope attribute declarations.

Example: The SchemaAttributeTest `schema-attribute(color)` matches a candidate attribute node if `color` is a top-level attribute declaration in the in-scope attribute declarations, the name of the candidate node is `color`, and the type annotation of the candidate node is the same as or derived from the schema type declared for the `color` attribute.

##### 2.5.5.7 Function Test

| [102]                                                                       | `FunctionTest`                                                              | ::=                                                                         | ` AnyFunctionTest \| TypedFunctionTest `                                    |                                                                             |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [103]                                                                       | `AnyFunctionTest`                                                           | ::=                                                                         | `"function" "(" "*" ")"`                                                    |                                                                             |
| [104]                                                                       | `TypedFunctionTest`                                                         | ::=                                                                         | `"function" "(" (SequenceType ("," SequenceType)*)? ")" "as" SequenceType ` |                                                                             |

A FunctionTest matches a [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31, potentially also checking its [function signature](https://www.w3.org/TR/xpath-datamodel-31/#dt-signature)DM31 . An AnyFunctionTest matches any item that is a function. A TypedFunctionTest matches an item if it is a [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31 and the function's type signature (as defined in [Section 2.8.1 Functions](https://www.w3.org/TR/xpath-datamodel-31/#function-items)DM31) is a subtype of the TypedFunctionTest.

Here are some examples of FunctionTests:

1. `function(*)` matches any function, including maps and arrays.
2. `function(int, int) as int` matches any [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31 with the function signature `function(int, int) as int`.
3. `function(xs:anyAtomicType) as item()*` matches any map, or any function with the required signature.
4. `function(xs:integer) as item()*` matches any array, or any function with the required signature.

##### 2.5.5.8 Map Test

| [105]                                              | `MapTest`                                          | ::=                                                | ` AnyMapTest \| TypedMapTest `                     |                                                    |
| -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- |
| [106]                                              | `AnyMapTest`                                       | ::=                                                | `"map" "(" "*" ")"`                                |                                                    |
| [107]                                              | `TypedMapTest`                                     | ::=                                                | `"map" "(" AtomicOrUnionType "," SequenceType ")"` |                                                    |

The MapTest `map(*)` matches any map. The MapTest `map(X, Y)` matches any map where the type of every key is an instance of `X` and the type of every value is an instance of `Y`.

Examples:

Given a map `$M` whose keys are integers and whose results are strings, such as `map{0:"no", 1:"yes"}`, consider the results of the following expressions:

- `$M instance of map(*)` returns `true()`
- `$M instance of map(xs:integer, xs:string)` returns `true()`
- `$M instance of map(xs:decimal, xs:anyAtomicType)` returns `true()`
- `not($M instance of map(xs:int, xs:string))` returns `true()`
- `not($M instance of map(xs:integer, xs:token))` returns `true()`

Because of the rules for subtyping of function types according to their signature, it follows that the item type `function(A) as item()*`, where A is an atomic type, also matches any map, regardless of the type of the keys actually found in the map. For example, a map whose keys are all strings can be supplied where the required type is `function(xs:integer) as item()*`; a call on the map that treats it as a function with an integer argument will always succeed, and will always return an empty sequence.

The function signature of a map matching type `map(K, V)`, treated as a function, is `function(xs:anyAtomicType) as V?`. It is thus always a subtype of `function(xs:anyAtomicType) as item()*` regardless of the actual types of the keys and values in the map. The rules for function coercion mean that any map can be supplied as a value in a context where the required type has a more specific return type, such as `function(xs:anyAtomicType) as xs:integer`, even when the map does not match in the sense required to satisfy the instance of operator. In such cases, a type error will only occur if an actual call on the map (treated as a function) returns a value that is not an instance of the required return type.

Examples:

- `$M instance of function(*)` returns `true()`
- `$M instance of function(xs:anyAtomicType) as item()*` returns `true()`
- `$M instance of function(xs:integer) as item()*` returns `true()`
- `$M instance of function(xs:int) as item()*` returns `true()`
- `$M instance of function(xs:string) as item()*` returns `true()`
- `not($M instance of function(xs:integer) as xs:string)` returns `true()`

**Note:**

The last case might seem surprising; however, function coercion ensures that `$M` can be used successfully anywhere that the required type is `function(xs:integer) as xs:string`.

##### 2.5.5.9 Array Test

| [108]                              | `ArrayTest`                        | ::=                                | ` AnyArrayTest \| TypedArrayTest ` |                                    |
| ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- |
| [109]                              | `AnyArrayTest`                     | ::=                                | `"array" "(" "*" ")"`              |                                    |
| [110]                              | `TypedArrayTest`                   | ::=                                | `"array" "(" SequenceType ")"`     |                                    |

The AnyArrayTest `array(*)` matches any array. The TypedArrayTest `array(X)` matches any array in which every array member matches the SequenceType `X`.

Examples:

- `[ 1, 2 ] instance array(*)` returns `true()`
- `[] instance of array(xs:string)` returns `true()`
- `[ "foo" ] instance of array(xs:string)` returns `true()`
- `[ "foo" ] instance of array(xs:integer)` returns `false()`
- `[(1,2),(3,4)] instance of array(xs:integer)` returns `false()`
- `[(1,2),(3,4)] instance of array(xs:integer+)` returns `true()`

An array also matches certain other ItemTypes, including:

- `item()`
- `function(*)`
- `function(xs:integer) as item()*`

The function signature of an array matching `array(X)`, treated as a function, is `function(xs:integer) as X`. It is thus always a subtype of `function(xs:integer) as item()*` regardless of the actual member types in the array. The rules for function coercion mean that any array can be supplied as a value in a context where the required type has a more specific return type, such as `function(xs:integer) as xs:integer`, even when the array does not match in the sense required to satisfy the instance of operator. In such cases, a type error will only occur if an actual call on the array (treated as a function) returns a value that is not an instance of the required return type.

#### 2.5.6 SequenceType Subtype Relationships

Given two sequence types, it is possible to determine if one is a subtype of the other. [Definition: A sequence type `A` is a **subtype** of a sequence type `B` if the judgement `subtype(A, B)` is true.] When the judgement `subtype(A, B)` is true, it is always the case that for any value `V`, `(V instance of A)` implies `(V instance of B)`.

##### 2.5.6.1 The judgement `subtype(A, B)`

The judgement `subtype(A, B)` determines if the sequence type `A` is a subtype of the sequence type `B`. `A` can either be `empty-sequence()`, `xs:error`, or an ItemType, `Ai`, possibly followed by an occurrence indicator. Similarly `B` can either be `empty-sequence()`, `xs:error`, or an ItemType, `Bi`, possibly followed by an occurrence indicator. The result of the `subtype(A, B)` judgement can be determined from the table below, which makes use of the auxiliary judgement `subtype-itemtype(Ai, Bi)` defined in **2.5.6.2 The judgement subtype-itemtype(Ai, Bi)**.
|                            | Sequence type `B`          |
| -------------------------- | -------------------------- |
| `empty-sequence()`         | `Bi?`                      | `Bi*`                      | `Bi`                       | `Bi+`                      | xs:error                   |
| Sequence type `A`          | `empty-sequence()`         | true                       | true                       | true                       | false                      | false                      | false                      |
| `Ai?`                      | false                      | `subtype-itemtype(Ai, Bi)` | `subtype-itemtype(Ai, Bi)` | false                      | false                      | false                      |
| `Ai*`                      | false                      | false                      | `subtype-itemtype(Ai, Bi)` | false                      | false                      | false                      |
| `Ai`                       | false                      | `subtype-itemtype(Ai, Bi)` | `subtype-itemtype(Ai, Bi)` | `subtype-itemtype(Ai, Bi)` | `subtype-itemtype(Ai, Bi)` | false                      |
| `Ai+`                      | false                      | false                      | `subtype-itemtype(Ai, Bi)` | false                      | `subtype-itemtype(Ai, Bi)` | false                      |
| `xs:error`                 | true                       | true                       | true                       | true                       | true                       | true                       |

`xs:error+` is treated the same way as `xs:error` in the above table. `xs:error?` and `xs:error*` are treated the same way as `empty-sequence()`.

##### 2.5.6.2 The judgement `subtype-itemtype(Ai, Bi)`

The judgement `subtype-itemtype(Ai, Bi)` determines if the ItemType `Ai` is a subtype of the ItemType `Bi`. `Ai` is a subtype of `Bi` if and only if at least one of the following conditions applies:

1. `Ai` and `Bi` are AtomicOrUnionTypes, and `derives-from(Ai, Bi)` returns `true`.
2. `Ai` is a pure union type, and every type `t` in the transitive membership of `Ai` satisfies `subtype-itemType(t, Bi)`.
3. `Ai` is `xs:error` and `Bi` is a generalized atomic type.
4. `Bi` is `item()`.
5. `Bi` is `node()`, and `Ai` is a KindTest.
6. `Bi` is `text()` and `Ai` is also `text()`.
7. `Bi` is `comment()` and `Ai` is also `comment()`.
8. `Bi` is `namespace-node()` and `Ai` is also `namespace-node()`.
9. `Bi` is `processing-instruction()` and `Ai` is either `processing-instruction()` or `processing-instruction(N)` for any name N.
10. `Bi` is `processing-instruction(Bn)`, and `Ai` is also `processing-instruction(Bn)`.
11. `Bi` is `document-node()` and `Ai` is either `document-node()` or `document-node(E)` for any ElementTest E.
12. `Bi` is `document-node(Be)` and `Ai` is `document-node(Ae)`, and `subtype-itemtype(Ae, Be)`.
13. `Bi` is either `element()` or `element(*)`, and `Ai` is an ElementTest.
14. `Bi` is either `element(Bn)` or `element(Bn, xs:anyType?)`, the expanded QName of `An` equals the expanded QName of `Bn`, and `Ai` is either `element(An)` or `element(An, T)` or `element(An, T?)` for any type T.
15. `Bi` is `element(Bn, Bt)`, the expanded QName of `An` equals the expanded QName of `Bn`, `Ai` is `element(An, At)`, and `derives-from(At, Bt)` returns `true`.
16. `Bi` is `element(Bn, Bt?)`, the expanded QName of `An` equals the expanded QName of `Bn`, `Ai` is either `element(An, At)` or `element(An, At?)`, and `derives-from(At, Bt)` returns `true`.
17. `Bi` is `element(*, Bt)`, `Ai` is either `element(*, At)` or `element(N, At)` for any name N, and `derives-from(At, Bt)` returns `true`.
18. `Bi` is `element(*, Bt?)`, `Ai` is either `element(*, At)`, `element(*, At?)`, `element(N, At)`, or `element(N, At?)` for any name N, and `derives-from(At, Bt)` returns `true`.
19. `Bi` is `schema-element(Bn)`, `Ai` is `schema-element(An)`, and every element declaration that is an actual member of the substitution group of `An` is also an actual member of the substitution group of `Bn`. **Note:** The fact that `P` is a member of the substitution group of `Q` does not mean that every element declaration in the substitution group of `P` is also in the substitution group of `Q`. For example, `Q` might block substitution of elements whose type is derived by extension, while `P` does not.
20. `Bi` is either `attribute()` or `attribute(*)`, and `Ai` is an AttributeTest.
21. `Bi` is either `attribute(Bn)` or `attribute(Bn, xs:anyType)`, the expanded QName of `An` equals the expanded QName of `Bn`, and `Ai` is either `attribute(An)`, or `attribute(An, T)` for any type T.
22. `Bi` is `attribute(Bn, Bt)`, the expanded QName of `An` equals the expanded QName of `Bn`, `Ai` is `attribute(An, At)`, and `derives-from(At, Bt)` returns `true`.
23. `Bi` is `attribute(*, Bt)`, `Ai` is either `attribute(*, At)`, or `attribute(N, At)` for any name N, and `derives-from(At, Bt)` returns `true`.
24. `Bi` is `schema-attribute(Bn)`, the expanded QName of `An` equals the expanded QName of `Bn`, and `Ai` is `schema-attribute(An)`.
25. `Bi` is ` function(*)`, `Ai` is a FunctionTest.
26. `Bi` is `function(Ba_1, Ba_2, ... Ba_N) as Br`, `Ai` is `function(Aa_1, Aa_2, ... Aa_M) as Ar`, where `N` (arity of Bi) equals `M` (arity of Ai); `subtype(Ar, Br)`; and for values of `I` between 1 and `N`, `subtype(Ba_I, Aa_I)`. **Note:** Function return types are covariant because this rule invokes subtype(Ar, Br) for return types. Function arguments are contravariant because this rule invokes subtype(Ba_I, Aa_I) for arguments.
27. `Ai` is `map(K, V)`, for any `K` and `V` and `Bi` is `map(*)`.
28. `Ai` is `map(Ka, Va)` and `Bi` is `map(Kb, Vb)`, where `subtype-itemtype(Ka, Kb)` and `subtype(Va, Vb)`.
29. `Ai` is `map(*)` (or, because of the transitivity rules, any other map type), and `Bi` is `function(*)`.
30. `Ai` is `map(*)` (or, because of the transitivity rules, any other map type), and `Bi` is `function(xs:anyAtomicType) as item()*`.
31. `Ai` is `array(X)` and `Bi` is `array(*)`.
32. `Ai` is `array(X)` and `Bi` is `array(Y)`, and `subtype(X, Y)` is true.
33. `Ai` is `array(*)` (or, because of the transitivity rules, any other array type) and `Bi` is `function(*)`.
34. `Ai` is `array(*)` (or, because of the transitivity rules, any other array type) and `Bi` is `function(xs:integer) as item()*`.
35. `Ai` is `map(K, V)`, and `Bi` is `function(xs:anyAtomicType) as V?`.
36. `Ai` is `array(X)` and `Bi` is `function(xs:integer) as X`.

#### 2.5.7 xs:error

The type `xs:error` has an empty value space; it never appears as a dynamic type or as the content type of a dynamic element or attribute type. It was defined in XML Schema in the interests of making the type system complete and closed, and it is also available in XPath 3.1 for similar reasons.

**Note:**

Even though it cannot occur in an instance, `xs:error` is a valid type name in a sequence type. The practical uses of `xs:error` as a sequence type are limited, but they do exist. For instance, an error handling function that always raises a dynamic error never returns a value, so `xs:error` is a good choice for the return type of the function.

The semantics of `xs:error` are well-defined as a consequence of the fact that `xs:error` is defined as a union type with no member types. For example:

- `$x instance of xs:error` always returns false, regardless of the value of `$x`.
- `$x cast as xs:error` fails dynamically with error [[err:FORG0001](https://www.w3.org/TR/xpath-functions-31/#ERRFORG0001)]FO31, regardless of the value of `$x`.
- `$x cast as xs:error?` raises a dynamic error [[err:FORG0001](https://www.w3.org/TR/xpath-functions-31/#ERRFORG0001)]FO31 if `exists($x)`, evaluates to the empty sequence if `empty($x)`.
- `xs:error($x)` has the same semantics as `$x cast as xs:error?` (see the previous bullet point)
- `$x castable as xs:error` evaluates to `false`, regardless of the value of `$x`.
- `$x treat as xs:error` raises a dynamic error [err:XPDY0050] if evaluated, regardless of the value of `$x`. It never fails statically.

All of the above examples assume that `$x` is actually evaluated. If the result of the query does not depend on the value of `$x`. the rules specified in **2.3.4 Errors and Optimization** permit an implementation to avoid evaluating `$x` and thus to avoid raising an error.

### 2.6 Comments

| [121]                                     | `Comment`                                 | ::=                                       | `"(:" (CommentContents \| Comment)* ":)"` | */* ws: explicit */*                      |
| ----------------------------------------- | ----------------------------------------- | ----------------------------------------- | ----------------------------------------- | ----------------------------------------- |
|                                           |                                           |                                           |                                           | */* gn: comments */*                      |
| [126]                                     | `CommentContents`                         | ::=                                       | `(Char+ - (Char* ('(:' \| ':)') Char*))`  |                                           |

Comments may be used to provide information relevant to programmers who read an expression. Comments are lexical constructs only, and do not affect expression processing.

Comments are strings, delimited by the symbols `(:` and `:)`. Comments may be nested.

A comment may be used anywhere ignorable whitespace is allowed (see **A.2.4.1 Default Whitespace Handling**).

The following is an example of a comment:

```
(: Houston, we have a problem :)
```

## 3 Expressions

This section discusses each of the basic kinds of expression. Each kind of expression has a name such as `PathExpr`, which is introduced on the left side of the grammar production that defines the expression. Since XPath 3.1 is a composable language, each kind of expression is defined in terms of other expressions whose operators have a higher precedence. In this way, the precedence of operators is represented explicitly in the grammar.

The order in which expressions are discussed in this document does not reflect the order of operator precedence. In general, this document introduces the simplest kinds of expressions first, followed by more complex expressions. For the complete grammar, see Appendix [**A XPath 3.1 Grammar**].

The highest-level symbol in the XPath grammar is XPath.

| [1]                                                          | `XPath`                                                      | ::=                                                          | ` Expr `                                                     |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [6]                                                          | `Expr`                                                       | ::=                                                          | ` ExprSingle ("," ExprSingle)*`                              |                                                              |
| [7]                                                          | `ExprSingle`                                                 | ::=                                                          | ` ForExpr \| LetExpr \| QuantifiedExpr \| IfExpr \| OrExpr ` |                                                              |

The XPath 3.1 operator that has lowest precedence is the comma operator, which is used to combine two operands to form a sequence. As shown in the grammar, a general expression (Expr) can consist of multiple ExprSingle operands, separated by commas. The name ExprSingle denotes an expression that does not contain a top-level comma operator (despite its name, an ExprSingle may evaluate to a sequence containing more than one item.)

The symbol ExprSingle is used in various places in the grammar where an expression is not allowed to contain a top-level comma. For example, each of the arguments of a function call must be an ExprSingle, because commas are used to separate the arguments of a function call.

After the comma, the expressions that have next lowest precedence are ForExpr, LetExpr, QuantifiedExpr, IfExpr, and OrExpr. Each of these expressions is described in a separate section of this document.

### 3.1 Primary Expressions

[Definition: **Primary expressions** are the basic primitives of the language. They include literals, variable references, context item expressions, and function calls. A primary expression may also be created by enclosing any expression in parentheses, which is sometimes helpful in controlling the precedence of operators.] Map and Array Constructors are described in **3.11 Maps and Arrays**.

| [56]                                                                             | `PrimaryExpr`                                                                    | ::=                                                                              | ` Literal \| VarRef \| ParenthesizedExpr \| ContextItemExpr \| FunctionCall \| F |                                                                                  |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [66]                                                                             | `FunctionItemExpr`                                                               | ::=                                                                              | ` NamedFunctionRef \| InlineFunctionExpr `                                       |                                                                                  |

#### 3.1.1 Literals

[Definition: A **literal** is a direct syntactic representation of an atomic value.] XPath 3.1 supports two kinds of literals: numeric literals and string literals.

| [57]                                                                 | `Literal`                                                            | ::=                                                                  | ` NumericLiteral \| StringLiteral `                                  |                                                                      |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [58]                                                                 | `NumericLiteral`                                                     | ::=                                                                  | ` IntegerLiteral \| DecimalLiteral \| DoubleLiteral `                |                                                                      |
| [113]                                                                | `IntegerLiteral`                                                     | ::=                                                                  | ` Digits `                                                           |                                                                      |
| [114]                                                                | `DecimalLiteral`                                                     | ::=                                                                  | `("." Digits) \| (Digits "." [0-9]*)`                                | */* ws: explicit */*                                                 |
| [115]                                                                | `DoubleLiteral`                                                      | ::=                                                                  | `(("." Digits) \| (Digits ("." [0-9]*)?)) [eE] [+-]? Digits `        | */* ws: explicit */*                                                 |
| [116]                                                                | `StringLiteral`                                                      | ::=                                                                  | `('"' (EscapeQuot \| [^"])* '"') \| ("'" (EscapeApos \| [^'])* "'")` | */* ws: explicit */*                                                 |
| [119]                                                                | `EscapeQuot`                                                         | ::=                                                                  | `'""'`                                                               |                                                                      |
| [120]                                                                | `EscapeApos`                                                         | ::=                                                                  | `"''"`                                                               |                                                                      |
| [125]                                                                | `Digits`                                                             | ::=                                                                  | `[0-9]+`                                                             |                                                                      |

The value of a **numeric literal** containing no "`.`" and no `e` or `E` character is an atomic value of type `xs:integer`. The value of a numeric literal containing "`.`" but no `e` or `E` character is an atomic value of type `xs:decimal`. The value of a numeric literal containing an `e` or `E` character is an atomic value of type `xs:double`. The value of the numeric literal is determined by casting it to the appropriate type according to the rules for casting from `xs:untypedAtomic` to a numeric type as specified in [Section 19.2 Casting from xs:string and xs:untypedAtomic](https://www.w3.org/TR/xpath-functions-31/#casting-from-strings)FO31.

**Note:**

The effect of the above rule is that in the case of an integer or decimal literal, a dynamic error [[err:FOAR0002](https://www.w3.org/TR/xpath-functions-31/#ERRFOAR0002)]FO31 will generally be raised if the literal is outside the range of values supported by the implementation (other options are available: see [Section 4.2 Arithmetic operators on numeric values](https://www.w3.org/TR/xpath-functions-31/#op.numeric)FO31 for details.)

The XML Schema specification allows implementations to impose a limit (which must not be less than 18 digits) on the size of integer and decimal values. The full range of values of built-in subtypes of `xs:integer`, such as `xs:long` and `xs:unsignedLong`, can be supported only if the limit is 20 digits or higher. Negative numbers such as the minimum value of `xs:long` (`-9223372036854775808`) are technically unary expressions rather than literals, but implementations may prefer to ensure that they are expressible.

The value of a **string literal** is an atomic value whose type is `xs:string` and whose value is the string denoted by the characters between the delimiting apostrophes or quotation marks. If the literal is delimited by apostrophes, two adjacent apostrophes within the literal are interpreted as a single apostrophe. Similarly, if the literal is delimited by quotation marks, two adjacent quotation marks within the literal are interpreted as one quotation mark.

Here are some examples of literal expressions:

- `"12.5"` denotes the string containing the characters '1', '2', '.', and '5'.
- `12` denotes the `xs:integer` value twelve.
- `12.5` denotes the `xs:decimal` value twelve and one half.
- `125E2` denotes the `xs:double` value twelve thousand, five hundred.
- `"He said, ""I don't like it."""` denotes a string containing two quotation marks and one apostrophe. **Note:** When XPath expressions are embedded in contexts where quotation marks have special significance, such as inside XML attributes, additional escaping may be needed.

The `xs:boolean` values `true` and `false` can be constructed by calls to the built-in functions `fn:true()` and `fn:false()`, respectively.

Values of other simple types can be constructed by calling the constructor function for the given type. The constructor functions for XML Schema built-in types are defined in [Section 18.1 Constructor functions for XML Schema built-in atomic types](https://www.w3.org/TR/xpath-functions-31/#constructor-functions-for-xsd-types)FO31. In general, the name of a constructor function for a given type is the same as the name of the type (including its namespace). For example:

- `xs:integer("12")` returns the integer value twelve.
- `xs:date("2001-08-25")` returns an item whose type is `xs:date` and whose value represents the date 25th August 2001.
- `xs:dayTimeDuration("PT5H")` returns an item whose type is `xs:dayTimeDuration` and whose value represents a duration of five hours.

Constructor functions can also be used to create special values that have no literal representation, as in the following examples:

- `xs:float("NaN")` returns the special floating-point value, "Not a Number."
- `xs:double("INF")` returns the special double-precision value, "positive infinity."

Constructor functions are available for all simple types, including union types. For example, if `my:dt` is a user-defined union type whose member types are `xs:date`, `xs:time`, and `xs:dateTime`, then the expression `my:dt("2011-01-10")` creates an atomic value of type `xs:date`. The rules follow XML Schema validation rules for union types: the effect is to choose the first member type that accepts the given string in its lexical space.

It is also possible to construct values of various types by using a `cast` expression. For example:

- `9 cast as hatsize` returns the atomic value `9` whose type is `hatsize`.

#### 3.1.2 Variable References

| [59]           | `VarRef`       | ::=            | `"$" VarName ` |                |
| -------------- | -------------- | -------------- | -------------- | -------------- |
| [60]           | `VarName`      | ::=            | ` EQName `     |                |

[Definition: A **variable reference** is an EQName preceded by a $-sign.] An unprefixed variable reference is in no namespace. Two variable references are equivalent if their expanded QNames are equal (as defined by the `eq` operator). The scope of a variable binding is defined separately for each kind of expression that can bind variables.

Every variable reference must match a name in the in-scope variables.

Every variable binding has a static scope. The scope defines where references to the variable can validly occur. It is a static error [err:XPST0008] to reference a variable that is not in scope. If a variable is bound in the static context for an expression, that variable is in scope for the entire expression except where it is occluded by another binding that uses the same name within that scope.

At evaluation time, the value of a variable reference is the value to which the relevant variable is bound.

#### 3.1.3 Parenthesized Expressions

| [61]                | `ParenthesizedExpr` | ::=                 | `"(" Expr? ")"`     |                     |
| ------------------- | ------------------- | ------------------- | ------------------- | ------------------- |

Parentheses may be used to override the precedence rules. For example, the expression `(2 + 4) * 5` evaluates to thirty, since the parenthesized expression `(2 + 4)` is evaluated first and its result is multiplied by five. Without parentheses, the expression `2 + 4 * 5` evaluates to twenty-two, because the multiplication operator has higher precedence than the addition operator.

Empty parentheses are used to denote an empty sequence, as described in **3.4.1 Constructing Sequences**.

#### 3.1.4 Context Item Expression

| [62]              | `ContextItemExpr` | ::=               | `"."`             |                   |
| ----------------- | ----------------- | ----------------- | ----------------- | ----------------- |

A **context item expression** evaluates to the context item, which may be either a node (as in the expression `fn:doc("bib.xml")/books/book[fn:count(./author)>1]`), or an atomic value or function (as in the expression `(1 to 100)[. mod 5 eq 0]`).

If the context item is [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31, a context item expression raises a dynamic error [err:XPDY0002].

#### 3.1.5 Static Function Calls

[Definition: The **built-in functions** are the functions defined in [XQuery and XPath Functions and Operators 3.1] in the `http://www.w3.org/2005/xpath-functions`, `http://www.w3.org/2001/XMLSchema`, `http://www.w3.org/2005/xpath-functions/math`, `http://www.w3.org/2005/xpath-functions/map`, and `http://www.w3.org/2005/xpath-functions/array` namespaces. ] The set of built-in functions is specified by the host language. Additional functions may be provided in the static context. XPath per se does not provide a way to declare named functions, but a host language may provide such a mechanism.

| [63]                                  | `FunctionCall`                        | ::=                                   | ` EQName ArgumentList `               | */* xgc: reserved-function-names */*  |
| ------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- |
|                                       |                                       |                                       |                                       | */* gn: parens */*                    |
| [50]                                  | `ArgumentList`                        | ::=                                   | `"(" (Argument ("," Argument)*)? ")"` |                                       |
| [64]                                  | `Argument`                            | ::=                                   | ` ExprSingle \| ArgumentPlaceholder ` |                                       |
| [65]                                  | `ArgumentPlaceholder`                 | ::=                                   | `"?"`                                 |                                       |

[Definition: A **static function call** consists of an EQName followed by a parenthesized list of zero or more arguments.] [Definition: An argument to a function call is either an **argument expression** or an ArgumentPlaceholder ("?").] If the EQName in a static function call is a lexical QName that has no namespace prefix, it is considered to be in the default function namespace.

If the expanded QName and number of arguments in a static function call do not match the name and arity of a function signature in the static context, a static error is raised [err:XPST0017].

[Definition: A static or dynamic function call is a **partial function application** if one or more arguments is an ArgumentPlaceholder. ]

Evaluation of function calls is described in **3.1.5.1 Evaluating Static and Dynamic Function Calls**.

Since the arguments of a function call are separated by commas, any argument expression that contains a top-level comma operator must be enclosed in parentheses. Here are some illustrative examples of static function calls:

- `my:three-argument-function(1, 2, 3)` denotes a static function call with three arguments.
- `my:two-argument-function((1, 2), 3)` denotes a static function call with two arguments, the first of which is a sequence of two values.
- `my:two-argument-function(1, ())` denotes a static function call with two arguments, the second of which is an empty sequence.
- `my:one-argument-function((1, 2, 3))` denotes a static function call with one argument that is a sequence of three values.
- `my:one-argument-function(( ))` denotes a static function call with one argument that is an empty sequence.
- `my:zero-argument-function( )` denotes a static function call with zero arguments.

##### 3.1.5.1 Evaluating Static and Dynamic Function Calls

When a static or dynamic function call FC is evaluated with respect to a static context SC and a dynamic context DC, the result is obtained as follows:

1. [Definition: The number of `Argument`s in an `ArgumentList` is its **arity**. ]
2. The function F to be called or partially applied is obtained as follows: If FC is a static function call: Using the expanded QName corresponding to FC's `EQName`, and the arity of FC's `ArgumentList`, the corresponding function is looked up in the named functions component of DC. Let F denote the function obtained. If FC is a dynamic function call: FC's base expression is evaluated with respect to SC and DC. If this yields a sequence consisting of a single function with the same arity as the arity of the `ArgumentList`, let F denote that function. Otherwise, a type error is raised [err:XPTY0004].
3. [Definition: Argument expressions are evaluated with respect to DC, producing **argument values**.] The order of argument evaluation is implementation-dependent and a function need not evaluate an argument if the function can evaluate its body without evaluating that argument.
4. Each argument value is converted to the corresponding parameter type in F's signature by applying the function conversion rules, resulting in a converted argument value.
5. The remainder depends on whether or not FC is a partial function application. If FC is a partial function application the result of the function call is a new function, which is a partially applied function. [Definition: A **partially applied function** is a function created by partial function application.] [Definition: In a partial function application, a **fixed position** is an argument/parameter position for which the `ArgumentList` has an argument expression (as opposed to an `ArgumentPlaceholder`).] A partial function application need not have any fixed positions. A partially applied function has the following properties (which are defined in [Section 2.8.1 Functions](https://www.w3.org/TR/xpath-datamodel-31/#function-items)DM31): **name**: Absent. **parameter names**: The parameter names of F, removing the parameter names at the fixed positions. (So the function's arity is the arity of F minus the number of fixed positions.) **signature**: The signature of F, removing the parameter type at each of the fixed positions. An implementation which can determine a more specific signature (for example, through use of type analysis) is permitted to do so. **implementation**: The implementation of F. If this is not an XPath 3.1 expression then the new function's implementation is associated with a static context and a dynamic context in one of two ways: if F's implementation is already associated with contexts, then those are used; otherwise, SC and DC are used. **nonlocal variable bindings**: The nonlocal variable bindings of F, plus, for each fixed position, a binding of the converted argument value to the corresponding parameter name. Example: Partial Application of an Anonymous Function In the following example, `$f` is an anonymous function, and `$paf` is a partially applied function created from `$f`. let $f := function ($seq, $delim) { fn:fold-left($seq, "", fn:concat(?, $delim, ?)) }, $paf := $f(?, ".") return $paf(1 to 5) `$paf` is also an anonymous function. It has one parameter, named `$delim`, which is taken from the corresponding parameter in `$f` (the other parameter is fixed). The implementation of `$paf` is the implementation of `$f`, which is `fn:fold-left($seq, "", fn:concat(?, $delim, ?))`. This implementation is associated with the `SC` and `DC` of the original expression in `$f`. The nonlocal bindings associate the value `"."` with the parameter `$delim`. Example: Partial Application of a Built-In Function The following partial function application creates a function that computes the sum of squares of a sequence. let $sum-of-squares := fn:fold-right(?, 0, function($a, $b) { $a*$a + $b }) return $sum-of-squares(1 to 3) `$sum-of-squares` is an anonymous function. It has one parameter, named `$seq`, which is taken from the corresponding parameter in `fn:fold-right` (the other two parameters are fixed). The implementation is the implementation of `fn:fold-right`, which is a built-in context-independent function. The nonlocal bindings contain the fixed bindings for the second and third parameters of `fn:fold-right`. Partial function application never returns a map or an array. If `$F` is a map or an array, then `$F(?)` is a partial function application that returns a function, but the function it returns is not a map nor an array. Example: Partial Application of a Map The following partial function application converts a map to an equivalent function that is not a map. let $a := map {"A": 1, "B": 2}(?) return $a("A") If FC is not a partial function application, the semantics of the call depend on the nature of function F's 'implementation' property (see [Section 2.8.1 Functions](https://www.w3.org/TR/xpath-datamodel-31/#function-items)DM31): **Note:** XPath 3.1 is a host language with respect to the data model. In XPath 3.1, if the implementation is a host language expression, then it is an XPath 3.1 expression. If F is a map, it is evaluated as described in **3.11.1.2 Map Lookup using Function Call Syntax**. If F is an array, it is evaluated as described in **3.11.2.2 Array Lookup using Function Call Syntax**. If F's implementation is an XPath 3.1 expression (e.g., F is an anonymous function, or a partial application of such a function): F's implementation is evaluated. The static context for this evaluation is the static context of the XPath 3.1 expression. The dynamic context for this evaluation is obtained by taking the dynamic context of the `InlineFunctionExpr` that contains the `FunctionBody`, and making the following changes: The focus (context item, context position, and context size) is [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31. In the variable values component of the dynamic context, each converted argument value is bound to the corresponding parameter name. When this is done, the converted argument value retains its most specific dynamic type, even though this type may be derived from the type of the formal parameter. For example, a function with a parameter `$p` of type `xs:decimal` can be invoked with an argument of type `xs:integer`, which is derived from `xs:decimal`. During the processing of this function call, the dynamic type of `$p` inside the body of the function is considered to be `xs:integer`. F's nonlocal variable bindings are also added to the variable values. (Note that the names of the nonlocal variables are by definition disjoint from the parameter names, so there can be no conflict.) The value returned by evaluating the function body is then converted to the declared return type of F by applying the function conversion rules. The result is then the result of evaluating FC. As with argument values, the value returned by a function retains its most specific type, which may be derived from the declared return type of F. For example, a function that has a declared return type of `xs:decimal` may in fact return a value of dynamic type `xs:integer`. Example: Derived Types and Nonlocal Variable Bindings `$incr` is a nonlocal variable that is available within the function because its variable binding has been added to the variable values of the function.. Even though the parameter and return type of this function are both `xs:decimal`, the more specific type `xs:integer` is preserved in both cases. let $incr := 1, $f := function ($i as xs:decimal) as xs:decimal { $i + $incr } return $f(5) Example: Using the Context Item in an Anonymous Function The following example will raise a dynamic error [err:XPDY0002]: let $vat := function() { @vat + @price } return shop/article/$vat() Instead, the context item can be used as an argument to the anonymous function: let $vat := function($art) { $art/@vat + $art/@price } return shop/article/$vat(.) Or, the value can be referenced as a nonlocal variable binding: let $ctx := shop/article, $vat := function() { for $a in $ctx return $a/@vat + $a/@price } return $vat() If F's implementation is not an XPath 3.1 expression (e.g., F is a built-in function or a host language function or a partial application of such a function): F's implementation is invoked in an implementation-dependent way. The processor makes the following information available to that invocation: the converted argument values; F's nonlocal variable bindings; and a static context and dynamic context. If F's implementation is associated with a static and a dynamic context, then these are supplied, otherwise SC and DC are supplied. How this information is used is implementation-defined. An API used to invoke external functions must state how the static and dynamic contexts are provided to a function that is invoked. The F&O specification states how the static and dynamic contexts are used in each function that it defines. A host language must state how the static and dynamic contexts are used in functions that it provides. The result is either an instance of F's return type or a dynamic error. This result is then the result of evaluating FC. Errors raised by built-in functions are defined in [XQuery and XPath Functions and Operators 3.1]. Errors raised by host-language-dependent functions are implementation-defined. Example: A Built-in Function The following function call uses the function [Section 2.5 fn:base-uri](https://www.w3.org/TR/xpath-functions-31/#func-base-uri)FO31. Use of `SC` and `DC` and errors raised by this function are all defined in [XQuery and XPath Functions and Operators 3.1]. fn:base-uri()

##### 3.1.5.2 Function Conversion Rules

[Definition: The **function conversion rules** are used to convert an argument value to its expected type; that is, to the declared type of the function parameter. ] The expected type is expressed as a sequence type. The function conversion rules are applied to a given value as follows:

- In a static function call, if XPath 1.0 compatibility mode is `true` and an argument of a static function is not of the expected type, then the following conversions are applied sequentially to the argument value V: If the expected type calls for a single item or optional single item (examples: `xs:string`, `xs:string?`, `xs:untypedAtomic`, `xs:untypedAtomic?`, `node()`, `node()?`, `item()`, `item()?`), then the value V is effectively replaced by V[1]. If the expected type is `xs:string` or `xs:string?`, then the value `V` is effectively replaced by `fn:string(V)`. If the expected type is `xs:double` or `xs:double?`, then the value `V` is effectively replaced by `fn:number(V)`. **Note:** XPath 1.0 compatibility mode has no effect on dynamic function calls, converting the result of an inline function to its required type, partial function application, or implicit function calls that occur when evaluating functions such as fn:for-each and fn:filter.
- If the expected type is a sequence of a generalized atomic type (possibly with an occurrence indicator `*`, `+`, or `?`), the following conversions are applied: Atomization is applied to the given value, resulting in a sequence of atomic values. Each item in the atomic sequence that is of type `xs:untypedAtomic` is cast to the expected generalized atomic type. If the item is of type `xs:untypedAtomic` and the expected type is namespace-sensitive, a type error [err:XPTY0117] is raised. For each numeric item in the atomic sequence that can be promoted to the expected atomic type using numeric promotion as described in **B.1 Type Promotion**, the promotion is done. For each item of type `xs:anyURI` in the atomic sequence that can be promoted to the expected atomic type using URI promotion as described in **B.1 Type Promotion**, the promotion is done.
- If the expected type is a TypedFunctionTest (possibly with an occurrence indicator `*`, `+`, or `?`), function coercion is applied to each function in the given value. **Note:** In XPath 3.1, maps and arrays are functions, so function coercion applies to them as well.
- If, after the above conversions, the resulting value does not match the expected type according to the rules for SequenceType Matching, a type error is raised [err:XPTY0004]. Note that the rules for SequenceType Matching permit a value of a derived type to be substituted for a value of its base type.

##### 3.1.5.3 Function Coercion

Function coercion is a transformation applied to [functions](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31 during application of the function conversion rules. [Definition: **Function coercion** wraps a [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31 in a new function with signature the same as the expected type. This effectively delays the checking of the argument and return types until the function is invoked.]

Function coercion is only defined to operate on [functions](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31. Given a function F, and an expected function type, function coercion proceeds as follows: If F and the expected type have different arity, a type error is raised [err:XPTY0004]. Otherwise, coercion returns a new function with the following properties (as defined in [Section 2.8.1 Functions](https://www.w3.org/TR/xpath-datamodel-31/#function-items)DM31):

- **name**: The name of F.
- **parameter names**: The parameter names of F.
- **signature**: `Annotations` is set to the annotations of F. `TypedFunctionTest` is set to the expected type.
- **implementation**: In effect, a `FunctionBody` that calls F, passing it the parameters of this new function, in order.
- **nonlocal variable bindings**: An empty mapping.

If the result of invoking the new function would necessarily result in a type error, that error may be raised during function coercion. It is implementation dependent whether this happens or not.

These rules have the following consequences:

- SequenceType matching of the function's arguments and result are delayed until that function is invoked.
- The function conversion rules applied to the function's arguments and result are defined by the SequenceType it has most recently been coerced to. Additional function conversion rules could apply when the wrapped function is invoked.
- If an implementation has static type information about a function, that can be used to type check the function's argument and return types during static analysis.

**Note:**

Although the semantics of function coercion are specified in terms of wrapping the functions, static typing will often be able to reduce the number of places where this is actually necessary.

Since maps and arrays are also functions in XPath 3.1, function coercion applies to them as well. For instance, consider the following expression:

```

let $m := map {
  "Monday" : true(),
  "Wednesday" : true(),
  "Friday" : true(),
  "Saturday" : false(),
  "Sunday" : false()
},
$days := ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
return fn:filter($days,$m)
```

The map `$m` has a function signature of `function(xs:anyAtomicType) as item()*`. When the `fn:filter()` function is called, the following occurs to the map:

1. The map `$m` is treated as `function ($f)`, equivalent to `map:get($m,?)`.
2. The function conversion rules result in applying function coercion to `$f`, wrapping `$f` in a new function (`$p`) with the signature `function(item()) as xs:boolean`.
3. `$p` is matched against the SequenceType `function(item()) as xs:boolean`, and succeeds.
4. When `$p` is invoked by `fn:filter()`, function conversion and SequenceType matching rules are applied to the argument, resulting in an `item()` value (`$a`) or a type error.
5. `$f` is invoked with `$a`, which returns an `xs:boolean` or the empty sequence.
6. `$p` applies function conversion rules and SequenceType matching to the result sequence from `$f`. When the result is an `xs:boolean` the SequenceType matching succeeds. When it is an empty sequence (such as when `$m` does not contain a key for `"Tuesday"`), SequenceType matching results in a type error [err:XPTY0004], since the expected type is `xs:boolean` and the actual type is an empty sequence.

Consider the following expression:

```

let $m := map {
"Monday" : true(),
"Tuesday" : false(),
"Wednesday" : true(),
"Thursday" : false(),
"Friday" : true(),
"Saturday" : false(),
"Sunday" : false()
}
let $days := ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
return fn:filter($days,$m)
```

The result of the expression is the sequence `("Monday", "Wednesday", "Friday")`

#### 3.1.6 Named Function References

| [67]                                 | `NamedFunctionRef`                   | ::=                                  | ` EQName "#" IntegerLiteral `        | */* xgc: reserved-function-names */* |
| ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ |
| [112]                                | `EQName`                             | ::=                                  | ` QName \| URIQualifiedName `        |                                      |

[Definition: A **named function reference** is an expression which evaluates to a named function. The name and arity of the returned function are known statically, and correspond to a function signature present in the static context; if the function is context dependent, then the returned function is associated with the static context of the named function reference and the dynamic context in which it is evaluated. ] [Definition: A **named function** is a function defined in the static context for the expression. To uniquely identify a particular named function, both its name as an expanded QName and its arity are required.]

If the EQName is a lexical QName that has no namespace prefix, it is considered to be in the default function namespace.

If the expanded QName and arity in a named function reference do not match the name and arity of a function signature in the static context, a static error is raised [err:XPST0017].

The value of a `NamedFunctionRef` is the function obtained by looking up the expanded QName and arity in the named functions component of the dynamic context.

Furthermore, if the function returned by the evaluation of a `NamedFunctionRef` has an implementation-dependent implementation, then the implementation of this function is associated with the static context of this `NamedFunctionRef` expression and with the dynamic context in which the `NamedFunctionRef` is evaluated.

The following are examples of named function references:

- `fn:abs#1` references the fn:abs function which takes a single argument.
- `fn:concat#5` references the fn:concat function which takes 5 arguments.
- `local:myfunc#2` references a function named local:myfunc which takes 2 arguments.

#### 3.1.7 Inline Function Expressions

| [68]                                                               | `InlineFunctionExpr`                                               | ::=                                                                | `"function" "(" ParamList? ")" ("as" SequenceType)? FunctionBody ` |                                                                    |
| ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| [2]                                                                | `ParamList`                                                        | ::=                                                                | ` Param ("," Param)*`                                              |                                                                    |
| [3]                                                                | `Param`                                                            | ::=                                                                | `"$" EQName TypeDeclaration?`                                      |                                                                    |
| [78]                                                               | `TypeDeclaration`                                                  | ::=                                                                | `"as" SequenceType `                                               |                                                                    |
| [4]                                                                | `FunctionBody`                                                     | ::=                                                                | ` EnclosedExpr `                                                   |                                                                    |

[Definition: An **inline function expression** creates an anonymous function defined directly in the inline function expression.] An inline function expression specifies the names and SequenceTypes of the parameters to the function, the SequenceType of the result, and the body of the function. [Definition: An **anonymous function** is a function with no name. Anonymous functions may be created, for example, by evaluating an inline function expression or by partial function application.]

If a function parameter is declared using a name but no type, its default type is item()*. If the result type is omitted from an inline function expression, its default result type is item()*.

The parameters of an inline function expression are considered to be variables whose scope is the function body. It is a static error [err:XQST0039] for an inline function expression to have more than one parameter with the same name.

The static context for the function body is inherited from the location of the inline function expression, with the exception of the static type of the context item which is initially [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31.

The variables in scope for the function body include all variables representing the function parameters, as well as all variables that are in scope for the inline function expression.

**Note:**

Function parameter names can mask variables that would otherwise be in scope for the function body.

The result of an inline function expression is a single function with the following properties (as defined in [Section 2.8.1 Functions](https://www.w3.org/TR/xpath-datamodel-31/#function-items)DM31):

- **name**: An absent name. Absent.
- **parameter names**: The parameter names in the `InlineFunctionExpr`'s `ParamList`.
- **signature**: A `FunctionTest` constructed from the `SequenceType`s in the `InlineFunctionExpr`. An implementation which can determine a more specific signature (for example, through use of type analysis of the function's body) is permitted to do so.
- **implementation**: The `InlineFunctionExpr`'s `FunctionBody`.
- **nonlocal variable bindings**: For each nonlocal variable, a binding of it to its value in the variable values component of the dynamic context of the `InlineFunctionExpr`.

The following are examples of some inline function expressions:

- This example creates a function that takes no arguments and returns a sequence of the first 6 primes: function() as xs:integer+ { 2, 3, 5, 7, 11, 13 }
- This example creates a function that takes two xs:double arguments and returns their product: function($a as xs:double, $b as xs:double) as xs:double { $a * $b }
- This example creates a function that returns its item()* argument: function($a) { $a }
- This example creates a sequence of functions each of which returns a different item from the default collection. collection()/(let $a := . return function() { $a })

#### 3.1.8 Enclosed Expressions
| [5]             | `EnclosedExpr`  | ::=             | `"{" Expr? "}"` |                 |
| --------------- | --------------- | --------------- | --------------- | --------------- |

[Definition: An **enclosed expression** is an instance of the EnclosedExpr production, which allows an optional expression within curly braces.] [Definition: In an enclosed expression, the optional expression enclosed in curly braces is called the **content expression**.] If the content expression is not provided explicitly, the content expression is `()`.

### 3.2 Postfix Expressions

| [49]                                                  | `PostfixExpr`                                         | ::=                                                   | ` PrimaryExpr (Predicate \| ArgumentList \| Lookup)*` |                                                       |
| ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- |
| [52]                                                  | `Predicate`                                           | ::=                                                   | `"[" Expr "]"`                                        |                                                       |
| [50]                                                  | `ArgumentList`                                        | ::=                                                   | `"(" (Argument ("," Argument)*)? ")"`                 |                                                       |

[Definition: An expression followed by a predicate (that is, `E1[E2]`) is referred to as a **filter expression**: its effect is to return those items from the value of `E1` that satisfy the predicate in E2.] Filter expressions are described in **3.2.1 Filter Expressions**

An expression (other than a raw EQName) followed by an argument list in parentheses (that is, `E1(E2, E3, ...)`) is referred to as a dynamic function call. Its effect is to evaluate `E1` to obtain a function, and then call that function, with `E2`, `E3`, `...` as arguments. Dynamic function calls are described in **3.2.2 Dynamic Function Calls**.

#### 3.2.1 Filter Expressions

| [49]                                                  | `PostfixExpr`                                         | ::=                                                   | ` PrimaryExpr (Predicate \| ArgumentList \| Lookup)*` |                                                       |
| ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- |
| [52]                                                  | `Predicate`                                           | ::=                                                   | `"[" Expr "]"`                                        |                                                       |

A filter expression consists of a base expression followed by a predicate, which is an expression written in square brackets. The result of the filter expression consists of the items returned by the base expression, filtered by applying the predicate to each item in turn. The ordering of the items returned by a filter expression is the same as their order in the result of the primary expression.

**Note:**

Where the expression before the square brackets is a ReverseStep or ForwardStep, the expression is technically not a filter expression but an AxisStep. There are minor differences in the semantics: see **3.3.3 Predicates within Steps**

Here are some examples of filter expressions:

- Given a sequence of products in a variable, return only those products whose price is greater than 100. $products[price gt 100]
- List all the integers from 1 to 100 that are divisible by 5. (See **3.4.1 Constructing Sequences** for an explanation of the `to` operator.) (1 to 100)[. mod 5 eq 0]
- The result of the following expression is the integer 25: (21 to 29)[5]
- The following example returns the fifth through ninth items in the sequence bound to variable `$orders`. $orders[fn:position() = (5 to 9)]
- The following example illustrates the use of a filter expression as a step in a path expression. It returns the last chapter or appendix within the book bound to variable `$book`: $book/(chapter | appendix)[fn:last()]

For each item in the input sequence, the predicate expression is evaluated using an **inner focus**, defined as follows: The context item is the item currently being tested against the predicate. The context size is the number of items in the input sequence. The context position is the position of the context item within the input sequence.

For each item in the input sequence, the result of the predicate expression is coerced to an `xs:boolean` value, called the **predicate truth value**, as described below. Those items for which the predicate truth value is `true` are retained, and those for which the predicate truth value is `false` are discarded.

The predicate truth value is derived by applying the following rules, in order:

1. If the value of the predicate expression is a singleton atomic value of a numeric type or derived from a numeric type, the predicate truth value is `true` if the value of the predicate expression is equal (by the `eq` operator) to the **context position**, and is `false` otherwise.
2. Otherwise, the predicate truth value is the effective boolean value of the predicate expression.

#### 3.2.2 Dynamic Function Calls

| [49]                                                  | `PostfixExpr`                                         | ::=                                                   | ` PrimaryExpr (Predicate \| ArgumentList \| Lookup)*` |                                                       |
| ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- |
| [50]                                                  | `ArgumentList`                                        | ::=                                                   | `"(" (Argument ("," Argument)*)? ")"`                 |                                                       |
| [64]                                                  | `Argument`                                            | ::=                                                   | ` ExprSingle \| ArgumentPlaceholder `                 |                                                       |
| [65]                                                  | `ArgumentPlaceholder`                                 | ::=                                                   | `"?"`                                                 |                                                       |

[Definition: A **dynamic function call** consists of a base expression that returns the function and a parenthesized list of zero or more arguments (argument expressions or ArgumentPlaceholders).]

A dynamic function call is evaluated as described in **3.1.5.1 Evaluating Static and Dynamic Function Calls**.

The following are examples of some dynamic function calls:

- This example invokes the function contained in $f, passing the arguments 2 and 3: $f(2, 3)
- This example fetches the second item from sequence $f, treats it as a function and invokes it, passing an `xs:string` argument: $f[2]("Hi there")
- This example invokes the function $f passing no arguments, and filters the result with a positional predicate: $f()[2]

### 3.3 Path Expressions

| [36]                                                                    | `PathExpr`                                                              | ::=                                                                     | `("/" RelativePathExpr?)\| ("//" RelativePathExpr)\| RelativePathExpr ` | */* xgc: leading-lone-slash */*                                         |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [37]                                                                    | `RelativePathExpr`                                                      | ::=                                                                     | ` StepExpr (("/" \| "//") StepExpr)*`                                   |                                                                         |

[Definition: A **path expression** can be used to locate nodes within trees. A path expression consists of a series of one or more steps, separated by "`/`" or "`//`", and optionally beginning with "`/`" or "`//`".] An initial "`/`" or "`//`" is an abbreviation for one or more initial steps that are implicitly added to the beginning of the path expression, as described below.

A path expression consisting of a single step is evaluated as described in **3.3.2 Steps**.

A "`/`" at the beginning of a path expression is an abbreviation for the initial step `(fn:root(self::node()) treat as document-node())/` (however, if the "`/`" is the entire path expression, the trailing "`/`" is omitted from the expansion.) The effect of this initial step is to begin the path at the root node of the tree that contains the context node. If the context item is not a node, a type error is raised [err:XPTY0020]. At evaluation time, if the root node of the context node is not a document node, a dynamic error is raised [err:XPDY0050].

A "`//`" at the beginning of a path expression is an abbreviation for the initial steps `(fn:root(self::node()) treat as document-node())/descendant-or-self::node()/` (however, "`//`" by itself is not a valid path expression [err:XPST0003].) The effect of these initial steps is to establish an initial node sequence that contains the root of the tree in which the context node is found, plus all nodes descended from this root. This node sequence is used as the input to subsequent steps in the path expression. If the context item is not a node, a type error is raised [err:XPTY0020]. At evaluation time, if the root node of the context node is not a document node, a dynamic error is raised [err:XPDY0050].

**Note:**

The descendants of a node do not include attribute nodesor namespace nodes.

A path expression that starts with "`/`" or "`//`" selects nodes starting from the root of the tree containing the context item; it is often referred to as an absolute path expression.

#### 3.3.1 Relative Path Expressions

| [37]                                  | `RelativePathExpr`                    | ::=                                   | ` StepExpr (("/" \| "//") StepExpr)*` |                                       |
| ------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- |

A relative path expression is a path expression that selects nodes within a tree by following a series of steps starting at the context node (which, unlike an absolute path expression, may be any node in a tree).

Each non-initial occurrence of "`//`" in a path expression is expanded as described in **3.3.5 Abbreviated Syntax**, leaving a sequence of steps separated by "`/`". This sequence of steps is then evaluated from left to right. So a path such as `E1/E2/E3/E4` is evaluated as `((E1/E2)/E3)/E4`. The semantics of a path expression are thus defined by the semantics of the binary "`/`" operator, which is defined in **3.3.1.1 Path operator (/)**.

**Note:**

Although the semantics describe the evaluation of a path with more than two steps as proceeding from left to right, the "`/`" operator is in most cases associative, so evaluation from right to left usually delivers the same result. The cases where "`/`" is not associative arise when the functions `fn:position()` and `fn:last()` are used: `A/B/position()` delivers a sequence of integers from 1 to the size of `(A/B)`, whereas `A/(B/position())` restarts the counting at each `B` element.

The following example illustrates the use of relative path expressions.

- `child::div1/child::para` Selects the `para` element children of the `div1` element children of the context node; that is, the `para` element grandchildren of the context node that have `div1` parents.

**Note:**

Since each step in a path provides context nodes for the following step, in effect, only the last step in a path is allowed to return a sequence of non-nodes.

**Note:**

The "`/`" character can be used either as a complete path expression or as the beginning of a longer path expression such as "`/*`". Also, "`*`" is both the multiply operator and a wildcard in path expressions. This can cause parsing difficulties when "`/`" appears on the left-hand side of "`*`". This is resolved using the leading-lone-slash constraint. For example, "`/*`" and "`/ *`" are valid path expressions containing wildcards, but "`/*5`" and "`/ * 5`" raise syntax errors. Parentheses must be used when "`/`" is used on the left-hand side of an operator, as in "`(/) * 5`". Similarly, "`4 + / * 5`" raises a syntax error, but "`4 + (/) * 5`" is a valid expression. The expression "`4 + /`" is also valid, because `/` does not occur on the left-hand side of the operator.

Similarly, in the expression `/ union /*`, "union" is interpreted as an element name rather than an operator. For it to be parsed as an operator, the expression should be written `(/) union /*`.

##### 3.3.1.1 Path operator (`/`)

The path operator "/" is used to build expressions for locating nodes within trees. Its left-hand side expression must return a sequence of nodes. The operator returns either a sequence of nodes, in which case it additionally performs document ordering and duplicate elimination, or a sequence of non-nodes.

Each operation `E1/E2` is evaluated as follows: Expression `E1` is evaluated, and if the result is not a (possibly empty) sequence `S` of nodes, a type error is raised [err:XPTY0019]. Each node in `S` then serves in turn to provide an inner focus (the node as the context item, its position in `S` as the context position, the length of `S` as the context size) for an evaluation of `E2`, as described in **2.1.2 Dynamic Context**. The sequences resulting from all the evaluations of `E2` are combined as follows:

1. If every evaluation of `E2` returns a (possibly empty) sequence of nodes, these sequences are combined, and duplicate nodes are eliminated based on node identity. The resulting node sequence is returned in document order.
2. If every evaluation of `E2` returns a (possibly empty) sequence of non-nodes, these sequences are concatenated, in order, and returned. The returned sequence preserves the orderings within and among the subsequences generated by the evaluations of `E2` .
3. If the multiple evaluations of `E2` return at least one node and at least one non-node, a type error is raised [err:XPTY0018].

**Note:**

The semantics of the path operator can also be defined using the simple map operator as follows (forming the union with an empty sequence `($R | ())` has the effect of eliminating duplicates and sorting nodes into document order):

```
E1/E2 ::= let $R := E1!E2
  return
    if (every $r in $R satisfies $r instance of node())
    then ($R|())
    else if (every $r in $R satisfies not($r instance of node()))
    then $R
    else error()
```

#### 3.3.2 Steps

| [38]                                           | `StepExpr`                                     | ::=                                            | ` PostfixExpr \| AxisStep `                    |                                                |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |
| [39]                                           | `AxisStep`                                     | ::=                                            | `(ReverseStep \| ForwardStep) PredicateList `  |                                                |
| [40]                                           | `ForwardStep`                                  | ::=                                            | `(ForwardAxis NodeTest) \| AbbrevForwardStep ` |                                                |
| [43]                                           | `ReverseStep`                                  | ::=                                            | `(ReverseAxis NodeTest) \| AbbrevReverseStep ` |                                                |
| [51]                                           | `PredicateList`                                | ::=                                            | ` Predicate*`                                  |                                                |

[Definition: A **step** is a part of a path expression that generates a sequence of items and then filters the sequence by zero or more predicates. The value of the step consists of those items that satisfy the predicates, working from left to right. A step may be either an axis step or a postfix expression.] Postfix expressions are described in **3.2 Postfix Expressions**.

[Definition: An **axis step** returns a sequence of nodes that are reachable from the context node via a specified axis. Such a step has two parts: an **axis**, which defines the "direction of movement" for the step, and a node test, which selects nodes based on their kind, name, and/or type annotation.] If the context item is a node, an axis step returns a sequence of zero or more nodes; otherwise, a type error is raised [err:XPTY0020]. The resulting node sequence is returned in document order. An axis step may be either a **forward step** or a **reverse step**, followed by zero or more predicates.

In the **abbreviated syntax** for a step, the axis can be omitted and other shorthand notations can be used as described in **3.3.5 Abbreviated Syntax**.

The unabbreviated syntax for an axis step consists of the axis name and node test separated by a double colon. The result of the step consists of the nodes reachable from the context node via the specified axis that have the node kind, name, and/or type annotation specified by the node test. For example, the step `child::para` selects the `para` element children of the context node: `child` is the name of the axis, and `para` is the name of the element nodes to be selected on this axis. The available axes are described in **3.3.2.1 Axes**. The available node tests are described in **3.3.2.2 Node Tests**. Examples of steps are provided in **3.3.4 Unabbreviated Syntax** and **3.3.5 Abbreviated Syntax**.

##### 3.3.2.1 Axes

| [41]                                                                             | `ForwardAxis`                                                                    | ::=                                                                              | `("child" "::")\| ("descendant" "::")\| ("attribute" "::")\| ("self" "::")\| ("d |                                                                                  |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [44]                                                                             | `ReverseAxis`                                                                    | ::=                                                                              | `("parent" "::")\| ("ancestor" "::")\| ("preceding-sibling" "::")\| ("preceding" |                                                                                  |

XPath defines a full set of **axes** for traversing documents, but a **host language** may define a subset of these axes. The following axes are defined:

- The `child` axis contains the children of the context node, which are the nodes returned by the [Section 5.3 children Accessor](https://www.w3.org/TR/xpath-datamodel-31/#dm-children)DM31. **Note:** Only document nodes and element nodes have children. If the context node is any other kind of node, or if the context node is an empty document or element node, then the child axis is an empty sequence. The children of a document node or element node may be element, processing instruction, comment, or text nodes. Attribute, namespace, and document nodes can never appear as children.
- the `descendant` axis is defined as the transitive closure of the child axis; it contains the descendants of the context node (the children, the children of the children, and so on)
- the `parent` axis contains the sequence returned by the [Section 5.11 parent Accessor](https://www.w3.org/TR/xpath-datamodel-31/#dm-parent)DM31, which returns the parent of the context node, or an empty sequence if the context node has no parent **Note:** An attribute node may have an element node as its parent, even though the attribute node is not a child of the element node.
- the `ancestor` axis is defined as the transitive closure of the parent axis; it contains the ancestors of the context node (the parent, the parent of the parent, and so on) **Note:** The ancestor axis includes the root node of the tree in which the context node is found, unless the context node is the root node.
- the `following-sibling` axis contains the context node's following siblings, those children of the context node's parent that occur after the context node in document order; if the context node is an attribute or namespace node, the `following-sibling` axis is empty
- the `preceding-sibling` axis contains the context node's preceding siblings, those children of the context node's parent that occur before the context node in document order; if the context node is an attribute or namespace node, the `preceding-sibling` axis is empty
- the `following` axis contains all nodes that are descendants of the root of the tree in which the context node is found, are not descendants of the context node, and occur after the context node in document order
- the `preceding` axis contains all nodes that are descendants of the root of the tree in which the context node is found, are not ancestors of the context node, and occur before the context node in document order
- the `attribute` axis contains the attributes of the context node, which are the nodes returned by the [Section 5.11 parent Accessor](https://www.w3.org/TR/xpath-datamodel-31/#dm-parent)DM31; the axis will be empty unless the context node is an element
- the `self` axis contains just the context node itself
- the `descendant-or-self` axis contains the context node and the descendants of the context node
- the `ancestor-or-self` axis contains the context node and the ancestors of the context node; thus, the ancestor-or-self axis will always include the root node
- the `namespace` axis contains the namespace nodes of the context node, which are the nodes returned by the [Section 5.7 namespace-nodes Accessor](https://www.w3.org/TR/xpath-datamodel-31/#dm-namespace-nodes)DM31; this axis is empty unless the context node is an element node. The `namespace` axis is deprecated as of XPath 2.0. If XPath 1.0 compatibility mode is `true`, the `namespace` axis must be supported. If XPath 1.0 compatibility mode is `false`, then support for the `namespace` axis is implementation-defined. An implementation that does not support the `namespace` axis when XPath 1.0 compatibility mode is `false` must raise a static error [err:XPST0010] if it is used. Applications needing information about the in-scope namespaces of an element should use the functions [Section 10.2.6 fn:in-scope-prefixes](https://www.w3.org/TR/xpath-functions-31/#func-in-scope-prefixes)FO31, and [Section 10.2.5 fn:namespace-uri-for-prefix](https://www.w3.org/TR/xpath-functions-31/#func-namespace-uri-for-prefix)FO31.

Axes can be categorized as **forward axes** and **reverse axes**. An axis that only ever contains the context node or nodes that are after the context node in document order is a forward axis. An axis that only ever contains the context node or nodes that are before the context node in document order is a reverse axis.

The `parent`, `ancestor`, `ancestor-or-self`, `preceding`, and `preceding-sibling` axes are reverse axes; all other axes are forward axes. The `ancestor`, `descendant`, `following`, `preceding` and `self` axes partition a document (ignoring attribute and namespace nodes): they do not overlap and together they contain all the nodes in the document.

[Definition: Every axis has a **principal node kind**. If an axis can contain elements, then the principal node kind is element; otherwise, it is the kind of nodes that the axis can contain.] Thus:

- For the attribute axis, the principal node kind is attribute.
- For the namespace axis, the principal node kind is namespace.
- For all other axes, the principal node kind is element.

##### 3.3.2.2 Node Tests

[Definition: A **node test** is a condition on the name, kind (element, attribute, text, document, comment, or processing instruction), and/or type annotation of a node. A node test determines which nodes contained by an axis are selected by a step.]

| [46]                                                           | `NodeTest`                                                     | ::=                                                            | ` KindTest \| NameTest `                                       |                                                                |
| -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| [47]                                                           | `NameTest`                                                     | ::=                                                            | ` EQName \| Wildcard `                                         |                                                                |
| [48]                                                           | `Wildcard`                                                     | ::=                                                            | `"*"\| (NCName ":*")\| ("*:" NCName)\| (BracedURILiteral "*")` | */* ws: explicit */*                                           |
| [112]                                                          | `EQName`                                                       | ::=                                                            | ` QName \| URIQualifiedName `                                  |                                                                |

[Definition: A node test that consists only of an EQName or a Wildcard is called a **name test**.] A name test that consists of an EQName is true if and only if the **kind** of the node is the principal node kind for the step axis and the expanded QName of the node is equal (as defined by the `eq` operator) to the expanded QName specified by the name test. For example, `child::para` selects the `para` element children of the context node; if the context node has no `para` children, it selects an empty set of nodes. `attribute::abc:href` selects the attribute of the context node with the QName `abc:href`; if the context node has no such attribute, it selects an empty set of nodes.

If the EQName is a lexical QName, it is resolved into an expanded QName using the statically known namespaces in the expression context. It is a static error [err:XPST0081] if the QName has a prefix that does not correspond to any statically known namespace. An unprefixed QName, when used as a name test on an axis whose principal node kind is element, has the namespace URI of the default element/type namespace in the expression context; otherwise, it has no namespace URI.

A name test is not satisfied by an element node whose name does not match the expanded QName of the name test, even if it is in a substitution group whose head is the named element.

A node test `*` is true for any node of the principal node kind of the step axis. For example, `child::*` will select all element children of the context node, and `attribute::*` will select all attributes of the context node.

A node test can have the form `NCName:*`. In this case, the prefix is expanded in the same way as with a lexical QName, using the statically known namespaces in the static context. If the prefix is not found in the statically known namespaces, a static error is raised [err:XPST0081]. The node test is true for any node of the principal node kind of the step axis whose expanded QName has the namespace URI to which the prefix is bound, regardless of the local part of the name.

A node test can contain a BracedURILiteral, e.g. `Q{http://example.com/msg}*` Such a node test is true for any node of the principal node kind of the step axis whose expanded QName has the namespace URI specified in the BracedURILiteral, regardless of the local part of the name.

A node test can also have the form `*:NCName`. In this case, the node test is true for any node of the principal node kind of the step axis whose local name matches the given NCName, regardless of its namespace or lack of a namespace.

[Definition: An alternative form of a node test called a **kind test** can select nodes based on their kind, name, and type annotation.] The syntax and semantics of a kind test are described in **2.5.4 SequenceType Syntax** and **2.5.5 SequenceType Matching**. When a kind test is used in a node test, only those nodes on the designated axis that match the kind test are selected. Shown below are several examples of kind tests that might be used in path expressions:

- `node()` matches any node.
- `text()` matches any text node.
- `comment()` matches any comment node.
- `namespace-node()` matches any namespace node.
- `element()` matches any element node.
- `schema-element(person)` matches any element node whose name is `person` (or is in the substitution group headed by `person`), and whose type annotation is the same as (or is derived from) the declared type of the `person` element in the in-scope element declarations.
- `element(person)` matches any element node whose name is `person`, regardless of its type annotation.
- `element(person, surgeon)` matches any non-nilled element node whose name is `person`, and whose type annotation is `surgeon` or is derived from `surgeon`.
- `element(*, surgeon)` matches any non-nilled element node whose type annotation is `surgeon` (or is derived from `surgeon`), regardless of its name.
- `attribute()` matches any attribute node.
- `attribute(price)` matches any attribute whose name is `price`, regardless of its type annotation.
- `attribute(*, xs:decimal)` matches any attribute whose type annotation is `xs:decimal` (or is derived from `xs:decimal`), regardless of its name.
- `document-node()` matches any document node.
- `document-node(element(book))` matches any document node whose content consists of a single element node that satisfies the kind test `element(book)`, interleaved with zero or more comments and processing instructions.

#### 3.3.3 Predicates within Steps

| [39]                                          | `AxisStep`                                    | ::=                                           | `(ReverseStep \| ForwardStep) PredicateList ` |                                               |
| --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- |
| [51]                                          | `PredicateList`                               | ::=                                           | ` Predicate*`                                 |                                               |
| [52]                                          | `Predicate`                                   | ::=                                           | `"[" Expr "]"`                                |                                               |

A predicate within a Step has similar syntax and semantics to a predicate within a filter expression. The only difference is in the way the context position is set for evaluation of the predicate.

For the purpose of evaluating the context position within a predicate, the input sequence is considered to be sorted as follows: into document order if the predicate is in a forward-axis step, into reverse document order if the predicate is in a reverse-axis step, or in its original order if the predicate is not in a step.

Here are some examples of axis steps that contain predicates:

- This example selects the second `chapter` element that is a child of the context node: child::chapter[2]
- This example selects all the descendants of the context node that are elements named `"toy"` and whose `color` attribute has the value `"red"`: descendant::toy[attribute::color = "red"]
- This example selects all the `employee` children of the context node that have both a `secretary` child element and an `assistant` child element: child::employee[secretary][assistant]

**Note:**

When using predicates with a sequence of nodes selected using a **reverse axis**, it is important to remember that the context positions for such a sequence are assigned in reverse document order. For example, `preceding::foo[1]` returns the first qualifying `foo` element in reverse document order, because the predicate is part of an axis step using a reverse axis. By contrast, `(preceding::foo)[1]` returns the first qualifying `foo` element in document order, because the parentheses cause `(preceding::foo)` to be parsed as a primary expression in which context positions are assigned in document order. Similarly, `ancestor::*[1]` returns the nearest ancestor element, because the `ancestor` axis is a reverse axis, whereas `(ancestor::*)[1]` returns the root element (first ancestor in document order).

The fact that a reverse-axis step assigns context positions in reverse document order for the purpose of evaluating predicates does not alter the fact that the final result of the step is always in document order.

#### 3.3.4 Unabbreviated Syntax

This section provides a number of examples of path expressions in which the axis is explicitly specified in each step. The syntax used in these examples is called the **unabbreviated syntax**. In many common cases, it is possible to write path expressions more concisely using an **abbreviated syntax**, as explained in **3.3.5 Abbreviated Syntax**.

- `child::para` selects the `para` element children of the context node
- `child::*` selects all element children of the context node
- `child::text()` selects all text node children of the context node
- `child::node()` selects all the children of the context node. Note that no attribute nodes are returned, because attributes are not children.
- `attribute::name` selects the `name` attribute of the context node
- `attribute::*` selects all the attributes of the context node
- `parent::node()` selects the parent of the context node. If the context node is an attribute node, this expression returns the element node (if any) to which the attribute node is attached.
- `descendant::para` selects the `para` element descendants of the context node
- `ancestor::div` selects all `div` ancestors of the context node
- `ancestor-or-self::div` selects the `div` ancestors of the context node and, if the context node is a `div` element, the context node as well
- `descendant-or-self::para` selects the `para` element descendants of the context node and, if the context node is a `para` element, the context node as well
- `self::para` selects the context node if it is a `para` element, and otherwise returns an empty sequence
- `child::chapter/descendant::para` selects the `para` element descendants of the `chapter` element children of the context node
- `child::*/child::para` selects all `para` grandchildren of the context node
- `/` selects the root of the tree that contains the context node, but raises a dynamic error if this root is not a document node
- `/descendant::para` selects all the `para` elements in the same document as the context node
- `/descendant::list/child::member` selects all the `member` elements that have a `list` parent and that are in the same document as the context node
- `child::para[fn:position() = 1]` selects the first `para` child of the context node
- `child::para[fn:position() = fn:last()]` selects the last `para` child of the context node
- `child::para[fn:position() = fn:last()-1]` selects the last but one `para` child of the context node
- `child::para[fn:position() > 1]` selects all the `para` children of the context node other than the first `para` child of the context node
- `following-sibling::chapter[fn:position() = 1]` selects the next `chapter` sibling of the context node
- `preceding-sibling::chapter[fn:position() = 1]` selects the previous `chapter` sibling of the context node
- `/descendant::figure[fn:position() = 42]` selects the forty-second `figure` element in the document containing the context node
- `/child::book/child::chapter[fn:position() = 5]/child::section[fn:position() = 2]` selects the second `section` of the fifth `chapter` of the `book` whose parent is the document node that contains the context node
- `child::para[attribute::type eq "warning"]` selects all `para` children of the context node that have a `type` attribute with value `warning`
- `child::para[attribute::type eq 'warning'][fn:position() = 5]` selects the fifth `para` child of the context node that has a `type` attribute with value `warning`
- `child::para[fn:position() = 5][attribute::type eq "warning"]` selects the fifth `para` child of the context node if that child has a `type` attribute with value `warning`
- `child::chapter[child::title = 'Introduction']` selects the `chapter` children of the context node that have one or more `title` children whose typed value is equal to the string `Introduction`
- `child::chapter[child::title]` selects the `chapter` children of the context node that have one or more `title` children
- `child::*[self::chapter or self::appendix]` selects the `chapter` and `appendix` children of the context node
- `child::*[self::chapter or self::appendix][fn:position() = fn:last()]` selects the last `chapter` or `appendix` child of the context node

#### 3.3.5 Abbreviated Syntax

| [42]                | `AbbrevForwardStep` | ::=                 | `"@"? NodeTest `    |                     |
| ------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| [45]                | `AbbrevReverseStep` | ::=                 | `".."`              |                     |

The abbreviated syntax permits the following abbreviations:

1. The attribute axis `attribute::` can be abbreviated by `@`. For example, a path expression `para[@type="warning"]` is short for `child::para[attribute::type="warning"]` and so selects `para` children with a `type` attribute with value equal to `warning`.
2. If the axis name is omitted from an axis step, the default axis is `child`, with two exceptions: (1) if the NodeTest in an axis step contains an AttributeTest or SchemaAttributeTest then the default axis is `attribute`; (2) if the NodeTest in an axis step is a NamespaceNodeTest then the default axis is `namespace` - in an implementation that does not support the namespace axis, an error is raised [err:XQST0134]. **Note:** The namespace axis is deprecated as of XPath 2.0, but required in some languages that use XPath, including XSLT. For example, the path expression `section/para` is an abbreviation for `child::section/child::para`, and the path expression `section/@id` is an abbreviation for `child::section/attribute::id`. Similarly, `section/attribute(id)` is an abbreviation for `child::section/attribute::attribute(id)`. Note that the latter expression contains both an axis specification and a node test.
3. Each non-initial occurrence of `//` is effectively replaced by `/descendant-or-self::node()/` during processing of a path expression. For example, `div1//para` is short for `child::div1/descendant-or-self::node()/child::para` and so will select all `para` descendants of `div1` children. **Note:** The path expression `//para[1]` does *not* mean the same as the path expression `/descendant::para[1]`. The latter selects the first descendant `para` element; the former selects all descendant `para` elements that are the first `para` children of their respective parents.
4. A step consisting of `..` is short for `parent::node()`. For example, `../title` is short for `parent::node()/child::title` and so will select the `title` children of the parent of the context node. **Note:** The expression `.`, known as a **context item expression**, is a primary expression, and is described in **3.1.4 Context Item Expression**.

Here are some examples of path expressions that use the abbreviated syntax:

- `para` selects the `para` element children of the context node
- `*` selects all element children of the context node
- `text()` selects all text node children of the context node
- `@name` selects the `name` attribute of the context node
- `@*` selects all the attributes of the context node
- `para[1]` selects the first `para` child of the context node
- `para[fn:last()]` selects the last `para` child of the context node
- `*/para` selects all `para` grandchildren of the context node
- `/book/chapter[5]/section[2]` selects the second `section` of the fifth `chapter` of the `book` whose parent is the document node that contains the context node
- `chapter//para` selects the `para` element descendants of the `chapter` element children of the context node
- `//para` selects all the `para` descendants of the root document node and thus selects all `para` elements in the same document as the context node
- `//@version` selects all the `version` attribute nodes that are in the same document as the context node
- `//list/member` selects all the `member` elements in the same document as the context node that have a `list` parent
- `.//para` selects the `para` element descendants of the context node
- `..` selects the parent of the context node
- `../@lang` selects the `lang` attribute of the parent of the context node
- `para[@type="warning"]` selects all `para` children of the context node that have a `type` attribute with value `warning`
- `para[@type="warning"][5]` selects the fifth `para` child of the context node that has a `type` attribute with value `warning`
- `para[5][@type="warning"]` selects the fifth `para` child of the context node if that child has a `type` attribute with value `warning`
- `chapter[title="Introduction"]` selects the `chapter` children of the context node that have one or more `title` children whose typed value is equal to the string `Introduction`
- `chapter[title]` selects the `chapter` children of the context node that have one or more `title` children
- `employee[@secretary and @assistant]` selects all the `employee` children of the context node that have both a `secretary` attribute and an `assistant` attribute
- `book/(chapter|appendix)/section` selects every `section` element that has a parent that is either a `chapter` or an `appendix` element, that in turn is a child of a `book` element that is a child of the context node.
- If `E` is any expression that returns a sequence of nodes, then the expression `E/.` returns the same nodes in document order, with duplicates eliminated based on node identity.

### 3.4 Sequence Expressions

XPath 3.1 supports operators to construct, filter, and combine sequences of items. Sequences are never nested—for example, combining the values `1`, `(2, 3)`, and `( )` into a single sequence results in the sequence `(1, 2, 3)`.

#### 3.4.1 Constructing Sequences

| [6]                                    | `Expr`                                 | ::=                                    | ` ExprSingle ("," ExprSingle)*`        |                                        |
| -------------------------------------- | -------------------------------------- | -------------------------------------- | -------------------------------------- | -------------------------------------- |
| [20]                                   | `RangeExpr`                            | ::=                                    | ` AdditiveExpr ( "to" AdditiveExpr )?` |                                        |

[Definition: One way to construct a sequence is by using the **comma operator**, which evaluates each of its operands and concatenates the resulting sequences, in order, into a single result sequence.] Empty parentheses can be used to denote an empty sequence.

A sequence may contain duplicate items, but a sequence is never an item in another sequence. When a new sequence is created by concatenating two or more input sequences, the new sequence contains all the items of the input sequences and its length is the sum of the lengths of the input sequences.

**Note:**

In places where the grammar calls for ExprSingle, such as the arguments of a function call, any expression that contains a top-level comma operator must be enclosed in parentheses.

Here are some examples of expressions that construct sequences:

- The result of this expression is a sequence of five integers: (10, 1, 2, 3, 4)
- This expression combines four sequences of length one, two, zero, and two, respectively, into a single sequence of length five. The result of this expression is the sequence `10, 1, 2, 3, 4`. (10, (1, 2), (), (3, 4))
- The result of this expression is a sequence containing all `salary` children of the context node followed by all `bonus` children. (salary, bonus)
- Assuming that `$price` is bound to the value `10.50`, the result of this expression is the sequence `10.50, 10.50`. ($price, $price)

A **range expression** can be used to construct a sequence of consecutive integers. Each of the operands of the `to` operator is converted as though it was an argument of a function with the expected parameter type `xs:integer?`. If either operand is an empty sequence, or if the integer derived from the first operand is greater than the integer derived from the second operand, the result of the range expression is an empty sequence. If the two operands convert to the same integer, the result of the range expression is that integer. Otherwise, the result is a sequence containing the two integer operands and every integer between the two operands, in increasing order.

- This example uses a range expression as one operand in constructing a sequence. It evaluates to the sequence `10, 1, 2, 3, 4`. (10, 1 to 4)
- This example constructs a sequence of length one containing the single integer `10`. 10 to 10
- The result of this example is a sequence of length zero. 15 to 10
- This example uses the `fn:reverse` function to construct a sequence of six integers in decreasing order. It evaluates to the sequence `15, 14, 13, 12, 11, 10`. fn:reverse(10 to 15)

#### 3.4.2 Combining Node Sequences

| [23]                                                              | `UnionExpr`                                                       | ::=                                                               | ` IntersectExceptExpr ( ("union" \| "\|") IntersectExceptExpr )*` |                                                                   |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| [24]                                                              | `IntersectExceptExpr`                                             | ::=                                                               | ` InstanceofExpr ( ("intersect" \| "except") InstanceofExpr )*`   |                                                                   |

XPath 3.1 provides the following operators for combining sequences of nodes:

- The `union` and `|` operators are equivalent. They take two node sequences as operands and return a sequence containing all the nodes that occur in either of the operands.
- The `intersect` operator takes two node sequences as operands and returns a sequence containing all the nodes that occur in both operands.
- The `except` operator takes two node sequences as operands and returns a sequence containing all the nodes that occur in the first operand but not in the second operand.

All these operators eliminate duplicate nodes from their result sequences based on node identity. The resulting sequence is returned in document order.

If an operand of `union`, `intersect`, or `except` contains an item that is not a node, a type error is raised [err:XPTY0004].

If an IntersectExceptExpr contains more than two InstanceofExprs, they are grouped from left to right. With a UnionExpr, it makes no difference how operands are grouped, the results are the same.

Here are some examples of expressions that combine sequences. Assume the existence of three element nodes that we will refer to by symbolic names A, B, and C. Assume that the variables `$seq1`, `$seq2` and `$seq3` are bound to the following sequences of these nodes:

- `$seq1` is bound to (A, B)
- `$seq2` is bound to (A, B)
- `$seq3` is bound to (B, C)

Then:

- `$seq1 union $seq2` evaluates to the sequence (A, B).
- `$seq2 union $seq3` evaluates to the sequence (A, B, C).
- `$seq1 intersect $seq2` evaluates to the sequence (A, B).
- `$seq2 intersect $seq3` evaluates to the sequence containing B only.
- `$seq1 except $seq2` evaluates to the empty sequence.
- `$seq2 except $seq3` evaluates to the sequence containing A only.

In addition to the sequence operators described here, see [Section 14 Functions and operators on sequences](https://www.w3.org/TR/xpath-functions-31/#sequence-functions)FO31 for functions defined on sequences.

### 3.5 Arithmetic Expressions

XPath 3.1 provides arithmetic operators for addition, subtraction, multiplication, division, and modulus, in their usual binary and unary forms.

| [21]                                                          | `AdditiveExpr`                                                | ::=                                                           | ` MultiplicativeExpr ( ("+" \| "-") MultiplicativeExpr )*`    |                                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| [22]                                                          | `MultiplicativeExpr`                                          | ::=                                                           | ` UnionExpr ( ("*" \| "div" \| "idiv" \| "mod") UnionExpr )*` |                                                               |
| [30]                                                          | `UnaryExpr`                                                   | ::=                                                           | `("-" \| "+")* ValueExpr `                                    |                                                               |
| [31]                                                          | `ValueExpr`                                                   | ::=                                                           | ` SimpleMapExpr `                                             |                                                               |

A subtraction operator must be preceded by whitespace if it could otherwise be interpreted as part of the previous token. For example, `a-b` will be interpreted as a name, but `a - b` and `a -b` will be interpreted as arithmetic expressions. (See **A.2.4 Whitespace Rules** for further details on whitespace handling.)

If an AdditiveExpr contains more than two MultiplicativeExprs, they are grouped from left to right. So, for instance,

```
A - B + C - D
```

is equivalent to

```
((A - B) + C) - D
```

Similarly, the operands of a MultiplicativeExpr are grouped from left to right.

The first step in evaluating an arithmetic expression is to evaluate its operands. The order in which the operands are evaluated is implementation-dependent.

If XPath 1.0 compatibility mode is `true`, each operand is evaluated by applying the following steps, in order:

1. Atomization is applied to the operand. The result of this operation is called the **atomized operand**.
2. If the atomized operand is an empty sequence, the result of the arithmetic expression is the `xs:double` value `NaN`, and the implementation need not evaluate the other operand or apply the operator. However, an implementation may choose to evaluate the other operand in order to determine whether it raises an error.
3. If the atomized operand is a sequence of length greater than one, any items after the first item in the sequence are discarded.
4. If the atomized operand is now an instance of type `xs:boolean`, `xs:string`, `xs:decimal` (including `xs:integer`), `xs:float`, or `xs:untypedAtomic`, then it is converted to the type `xs:double` by applying the `fn:number` function. (Note that `fn:number` returns the value `NaN` if its operand cannot be converted to a number.)

If XPath 1.0 compatibility mode is `false`, each operand is evaluated by applying the following steps, in order:

1. Atomization is applied to the operand. The result of this operation is called the **atomized operand**.
2. If the atomized operand is an empty sequence, the result of the arithmetic expression is an empty sequence, and the implementation need not evaluate the other operand or apply the operator. However, an implementation may choose to evaluate the other operand in order to determine whether it raises an error.
3. If the atomized operand is a sequence of length greater than one, a type error is raised [err:XPTY0004].
4. If the atomized operand is of type `xs:untypedAtomic`, it is cast to `xs:double`. If the cast fails, a dynamic error is raised. [[err:FORG0001](https://www.w3.org/TR/xpath-functions-31/#ERRFORG0001)]FO31

After evaluation of the operands, if the types of the operands are a valid combination for the given arithmetic operator, the operator is applied to the operands, resulting in an atomic value or a dynamic error (for example, an error might result from dividing by zero.) The combinations of atomic types that are accepted by the various arithmetic operators, and their respective result types, are listed in **B.2 Operator Mapping** together with the operator functions that define the semantics of the operator for each type combination, including the dynamic errors that can be raised by the operator. The definitions of the operator functions are found in [XQuery and XPath Functions and Operators 3.1].

If the types of the operands, after evaluation, are not a valid combination for the given operator, according to the rules in **B.2 Operator Mapping**, a type error is raised [err:XPTY0004].

XPath 3.1 supports two division operators named `div` and `idiv`. Each of these operators accepts two operands of any numeric type. The semantics of `div` are defined in [Section 4.2.5 op:numeric-integer-divide](https://www.w3.org/TR/xpath-functions-31/#func-numeric-integer-divide)FO31. The semantics of `idiv` are defined in [Section 4.2.4 op:numeric-divide](https://www.w3.org/TR/xpath-functions-31/#func-numeric-divide)FO31.

Here are some examples of arithmetic expressions:

- The first expression below returns the `xs:decimal` value `-1.5`, and the second expression returns the `xs:integer` value `-1`: -3 div 2 -3 idiv 2
- Subtraction of two date values results in a value of type `xs:dayTimeDuration`: $emp/hiredate - $emp/birthdate
- This example illustrates the difference between a subtraction operator and a hyphen: $unit-price - $unit-discount
- Unary operators have higher precedence than binary operators (other than "`!`", "`/`", and "`[]`"), subject of course to the use of parentheses. Therefore, the following two examples have different meanings: -$bellcost + $whistlecost -($bellcost + $whistlecost)

**Note:**

Multiple consecutive unary arithmetic operators are permitted.

### 3.6 String Concatenation Expressions

| [19]                               | `StringConcatExpr`                 | ::=                                | ` RangeExpr ( "\|\|" RangeExpr )*` |                                    |
| ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- |

String concatenation expressions allow the string representations of values to be concatenated. In XPath 3.1, `$a || $b` is equivalent to `fn:concat($a, $b)`. The following expression evaluates to the string `concatenate`:

```
"con" || "cat" || "enate"
```

### 3.7 Comparison Expressions

Comparison expressions allow two values to be compared. XPath 3.1 provides three kinds of comparison expressions, called value comparisons, general comparisons, and node comparisons.

| [18]                                                                             | `ComparisonExpr`                                                                 | ::=                                                                              | ` StringConcatExpr ( (ValueComp \| GeneralComp \| NodeComp) StringConcatExpr )?` |                                                                                  |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [33]                                                                             | `ValueComp`                                                                      | ::=                                                                              | `"eq" \| "ne" \| "lt" \| "le" \| "gt" \| "ge"`                                   |                                                                                  |
| [32]                                                                             | `GeneralComp`                                                                    | ::=                                                                              | `"=" \| "!=" \| "<" \| "<=" \| ">" \| ">="`                                      |                                                                                  |
| [34]                                                                             | `NodeComp`                                                                       | ::=                                                                              | `"is" \| "<<" \| ">>"`                                                           |                                                                                  |

**Note:**

When an XPath expression is written within an XML document, the XML escaping rules for special characters must be followed; thus "`<`" must be written as "`&lt;`".

#### 3.7.1 Value Comparisons

The value comparison operators are `eq`, `ne`, `lt`, `le`, `gt`, and `ge`. Value comparisons are used for comparing single values.

The first step in evaluating a value comparison is to evaluate its operands. The order in which the operands are evaluated is implementation-dependent. Each operand is evaluated by applying the following steps, in order:

1. Atomization is applied to each operand. The result of this operation is called the **atomized operand**.
2. If an atomized operand is an empty sequence, the result of the value comparison is an empty sequence, and the implementation need not evaluate the other operand or apply the operator. However, an implementation may choose to evaluate the other operand in order to determine whether it raises an error.
3. If an atomized operand is a sequence of length greater than one, a type error is raised [err:XPTY0004].
4. If an atomized operand is of type `xs:untypedAtomic`, it is cast to `xs:string`. **Note:** The purpose of this rule is to make value comparisons transitive. Users should be aware that the general comparison operators have a different rule for casting of `xs:untypedAtomic` operands. Users should also be aware that transitivity of value comparisons may be compromised by loss of precision during type conversion (for example, two `xs:integer` values that differ slightly may both be considered equal to the same `xs:float` value because `xs:float` has less precision than `xs:integer`).
5. If the two operands are instances of different primitive types (meaning the 19 primitive types defined in [Section 3.2 Primitive datatypes](https://www.w3.org/TR/xmlschema-2/#built-in-primitive-datatypes)XS2), then: If each operand is an instance of one of the types `xs:string` or `xs:anyURI`, then both operands are cast to type `xs:string`. If each operand is an instance of one of the types `xs:decimal` or `xs:float`, then both operands are cast to type `xs:float`. If each operand is an instance of one of the types `xs:decimal`, `xs:float`, or `xs:double`, then both operands are cast to type `xs:double`. Otherwise, a type error is raised [err:XPTY0004]. **Note:** The primitive type of an `xs:integer` value for this purpose is `xs:decimal`.
6. Finally, if the types of the operands are a valid combination for the given operator, the operator is applied to the operands.

The combinations of atomic types that are accepted by the various value comparison operators, and their respective result types, are listed in **B.2 Operator Mapping** together with the operator functions that define the semantics of the operator for each type combination. The definitions of the operator functions are found in [XQuery and XPath Functions and Operators 3.1].

Informally, if both atomized operands consist of exactly one atomic value, then the result of the comparison is `true` if the value of the first operand is (equal, not equal, less than, less than or equal, greater than, greater than or equal) to the value of the second operand; otherwise the result of the comparison is `false`.

If the types of the operands, after evaluation, are not a valid combination for the given operator, according to the rules in **B.2 Operator Mapping**, a type error is raised [err:XPTY0004].

Here are some examples of value comparisons:

- The following comparison atomizes the node(s) that are returned by the expression `$book/author`. The comparison is true only if the result of atomization is the value "Kennedy" as an instance of `xs:string` or `xs:untypedAtomic`. If the result of atomization is an empty sequence, the result of the comparison is an empty sequence. If the result of atomization is a sequence containing more than one value, a type error is raised [err:XPTY0004]. $book1/author eq "Kennedy"
- The following comparison is `true` because atomization converts an array to its member sequence: [ "Kennedy" ] eq "Kennedy"
- The following path expression contains a predicate that selects products whose weight is greater than 100. For any product that does not have a `weight` subelement, the value of the predicate is the empty sequence, and the product is not selected. This example assumes that `weight` is a validated element with a numeric type. //product[weight gt 100]
- The following comparison is true if `my:hatsize` and `my:shoesize` are both user-defined types that are derived by restriction from a primitive numeric type: my:hatsize(5) eq my:shoesize(5)
- The following comparison is true. The `eq` operator compares two QNames by performing codepoint-comparisons of their namespace URIs and their local names, ignoring their namespace prefixes. fn:QName("http://example.com/ns1", "this:color") eq fn:QName("http://example.com/ns1", "that:color")

#### 3.7.2 General Comparisons

The general comparison operators are `=`, `!=`, `<`, `<=`, `>`, and `>=`. General comparisons are existentially quantified comparisons that may be applied to operand sequences of any length. The result of a general comparison that does not raise an error is always `true` or `false`.

If XPath 1.0 compatibility mode is `true`, a general comparison is evaluated by applying the following rules, in order:

1. If either operand is a single atomic value that is an instance of `xs:boolean`, then the other operand is converted to `xs:boolean` by taking its effective boolean value.
2. Atomization is applied to each operand. After atomization, each operand is a sequence of atomic values.
3. If the comparison operator is `<`, `<=`, `>`, or `>=`, then each item in both of the operand sequences is converted to the type `xs:double` by applying the `fn:number` function. (Note that `fn:number` returns the value `NaN` if its operand cannot be converted to a number.)
4. The result of the comparison is `true` if and only if there is a pair of atomic values, one in the first operand sequence and the other in the second operand sequence, that have the required **magnitude relationship**. Otherwise the result of the comparison is `false` or an error. The **magnitude relationship** between two atomic values is determined by applying the following rules. If a `cast` operation called for by these rules is not successful, a dynamic error is raised. [[err:FORG0001](https://www.w3.org/TR/xpath-functions-31/#ERRFORG0001)]FO31 If at least one of the two atomic values is an instance of a numeric type, then both atomic values are converted to the type `xs:double` by applying the `fn:number` function. If at least one of the two atomic values is an instance of `xs:string`, or if both atomic values are instances of `xs:untypedAtomic`, then both atomic values are cast to the type `xs:string`. If one of the atomic values is an instance of `xs:untypedAtomic` and the other is not an instance of `xs:string`, `xs:untypedAtomic`, or any numeric type, then the `xs:untypedAtomic` value is cast to the dynamic type of the other value. After performing the conversions described above, the atomic values are compared using one of the value comparison operators `eq`, `ne`, `lt`, `le`, `gt`, or `ge`, depending on whether the general comparison operator was `=`, `!=`, `<`, `<=`, `>`, or `>=`. The values have the required **magnitude relationship** if and only if the result of this value comparison is `true`.

If XPath 1.0 compatibility mode is `false`, a general comparison is evaluated by applying the following rules, in order:

1. Atomization is applied to each operand. After atomization, each operand is a sequence of atomic values.
2. The result of the comparison is `true` if and only if there is a pair of atomic values, one in the first operand sequence and the other in the second operand sequence, that have the required **magnitude relationship**. Otherwise the result of the comparison is `false` or an error. The **magnitude relationship** between two atomic values is determined by applying the following rules. If a `cast` operation called for by these rules is not successful, a dynamic error is raised. [[err:FORG0001](https://www.w3.org/TR/xpath-functions-31/#ERRFORG0001)]FO31 If both atomic values are instances of `xs:untypedAtomic`, then the values are cast to the type `xs:string`. If exactly one of the atomic values is an instance of `xs:untypedAtomic`, it is cast to a type depending on the other value's dynamic type T according to the following rules, in which V denotes the value to be cast: If T is a numeric type or is derived from a numeric type, then V is cast to `xs:double`. If T is `xs:dayTimeDuration` or is derived from `xs:dayTimeDuration`, then V is cast to `xs:dayTimeDuration`. If T is `xs:yearMonthDuration` or is derived from `xs:yearMonthDuration`, then V is cast to `xs:yearMonthDuration`. In all other cases, V is cast to the primitive base type of T. **Note:** The special treatment of the duration types is required to avoid errors that may arise when comparing the primitive type `xs:duration` with any duration type. After performing the conversions described above, the atomic values are compared using one of the value comparison operators `eq`, `ne`, `lt`, `le`, `gt`, or `ge`, depending on whether the general comparison operator was `=`, `!=`, `<`, `<=`, `>`, or `>=`. The values have the required **magnitude relationship** if and only if the result of this value comparison is `true`.

When evaluating a general comparison in which either operand is a sequence of items, an implementation may return `true` as soon as it finds an item in the first operand and an item in the second operand that have the required **magnitude relationship**. Similarly, a general comparison may raise a dynamic error as soon as it encounters an error in evaluating either operand, or in comparing a pair of items from the two operands. As a result of these rules, the result of a general comparison is not deterministic in the presence of errors.

Here are some examples of general comparisons:

- The following comparison is true if the typed value of any `author` subelement of `$book1` is "Kennedy" as an instance of `xs:string` or `xs:untypedAtomic`: $book1/author = "Kennedy"
- The following comparison is `true` because atomization converts an array to its member sequence: [ "Obama", "Nixon", "Kennedy" ] = "Kennedy"
- The following example contains three general comparisons. The value of the first two comparisons is `true`, and the value of the third comparison is `false`. This example illustrates the fact that general comparisons are not transitive. (1, 2) = (2, 3) (2, 3) = (3, 4) (1, 2) = (3, 4)
- The following example contains two general comparisons, both of which are `true`. This example illustrates the fact that the `=` and `!=` operators are not inverses of each other. (1, 2) = (2, 3) (1, 2) != (2, 3)
- Suppose that `$a`, `$b`, and `$c` are bound to element nodes with type annotation `xs:untypedAtomic`, with string values "`1`", "`2`", and "`2.0`" respectively. Then `($a, $b) = ($c, 3.0)` returns `false`, because `$b` and `$c` are compared as strings. However, `($a, $b) = ($c, 2.0)` returns `true`, because `$b` and `2.0` are compared as numbers.

#### 3.7.3 Node Comparisons

Node comparisons are used to compare two nodes, by their identity or by their document order. The result of a node comparison is defined by the following rules:

1. The operands of a node comparison are evaluated in implementation-dependent order.
2. If either operand is an empty sequence, the result of the comparison is an empty sequence, and the implementation need not evaluate the other operand or apply the operator. However, an implementation may choose to evaluate the other operand in order to determine whether it raises an error.
3. Each operand must be either a single node or an empty sequence; otherwise a type error is raised [err:XPTY0004].
4. A comparison with the `is` operator is `true` if the two operand nodes are the same node; otherwise it is `false`. See [XQuery and XPath Data Model (XDM) 3.1] for the definition of node identity.
5. A comparison with the `<<` operator returns `true` if the left operand node precedes the right operand node in document order; otherwise it returns `false`.
6. A comparison with the `>>` operator returns `true` if the left operand node follows the right operand node in document order; otherwise it returns `false`.

Here are some examples of node comparisons:

- The following comparison is true only if the left and right sides each evaluate to exactly the same single node: /books/book[isbn="1558604820"] is /books/book[call="QA76.9 C3845"]
- The following comparison is true only if the node identified by the left side occurs before the node identified by the right side in document order: /transactions/purchase[parcel="28-451"] << /transactions/sale[parcel="33-870"]

### 3.8 Logical Expressions

A **logical expression** is either an **and-expression** or an **or-expression**. If a logical expression does not raise an error, its value is always one of the boolean values `true` or `false`.

| [16]                                        | `OrExpr`                                    | ::=                                         | ` AndExpr ( "or" AndExpr )*`                |                                             |
| ------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ------------------------------------------- |
| [17]                                        | `AndExpr`                                   | ::=                                         | ` ComparisonExpr ( "and" ComparisonExpr )*` |                                             |

The first step in evaluating a logical expression is to find the effective boolean value of each of its operands (see **2.4.3 Effective Boolean Value**).

The value of an and-expression is determined by the effective boolean values (EBV's) of its operands, as shown in the following table:
| AND:                                                                             | EBV2 = `true`                                                                    | EBV2 = `false`                                                                   | error in EBV2                                                                    |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| EBV1 = `true`                                                                    | `true`                                                                           | `false`                                                                          | error                                                                            |
| EBV1 = `false`                                                                   | `false`                                                                          | `false`                                                                          | if XPath 1.0 compatibility mode is `true`, then `false`; otherwise either `false |
| error in EBV1                                                                    | error                                                                            | if XPath 1.0 compatibility mode is `true`, then error; otherwise either `false`  | error                                                                            |

The value of an or-expression is determined by the effective boolean values (EBV's) of its operands, as shown in the following table:
| OR:                                                                              | EBV2 = `true`                                                                    | EBV2 = `false`                                                                   | error in EBV2                                                                    |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| EBV1 = `true`                                                                    | `true`                                                                           | `true`                                                                           | if XPath 1.0 compatibility mode is `true`, then `true`; otherwise either `true`  |
| EBV1 = `false`                                                                   | `true`                                                                           | `false`                                                                          | error                                                                            |
| error in EBV1                                                                    | if XPath 1.0 compatibility mode is `true`, then error; otherwise either `true` o | error                                                                            | error                                                                            |

If XPath 1.0 compatibility mode is `true`, the order in which the operands of a logical expression are evaluated is effectively prescribed. Specifically, it is defined that when there is no need to evaluate the second operand in order to determine the result, then no error can occur as a result of evaluating the second operand.

If XPath 1.0 compatibility mode is `false`, the order in which the operands of a logical expression are evaluated is implementation-dependent. In this case, an or-expression can return `true` if the first expression evaluated is true, and it can raise an error if evaluation of the first expression raises an error. Similarly, an and-expression can return `false` if the first expression evaluated is false, and it can raise an error if evaluation of the first expression raises an error. As a result of these rules, a logical expression is not deterministic in the presence of errors, as illustrated in the examples below.

Here are some examples of logical expressions:

- The following expressions return `true`: 1 eq 1 and 2 eq 2 1 eq 1 or 2 eq 3
- The following expression may return either `false` or raise a dynamic error (in XPath 1.0 compatibility mode, the result must be `false`): 1 eq 2 and 3 idiv 0 = 1
- The following expression may return either `true` or raise a dynamic error (in XPath 1.0 compatibility mode, the result must be `true`): 1 eq 1 or 3 idiv 0 = 1
- The following expression must raise a dynamic error: 1 eq 1 and 3 idiv 0 = 1

In addition to and- and or-expressions, XPath 3.1 provides a function named `fn:not` that takes a general sequence as parameter and returns a boolean value. The `fn:not` function is defined in [XQuery and XPath Functions and Operators 3.1]. The `fn:not` function reduces its parameter to an effective boolean value. It then returns `true` if the effective boolean value of its parameter is `false`, and `false` if the effective boolean value of its parameter is `true`. If an error is encountered in finding the effective boolean value of its operand, `fn:not` raises the same error.

### 3.9 For Expressions

XPath provides an iteration facility called a **for expression**.

| [8]                                              | `ForExpr`                                        | ::=                                              | ` SimpleForClause "return" ExprSingle `          |                                                  |
| ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ |
| [9]                                              | `SimpleForClause`                                | ::=                                              | `"for" SimpleForBinding ("," SimpleForBinding)*` |                                                  |
| [10]                                             | `SimpleForBinding`                               | ::=                                              | `"$" VarName "in" ExprSingle `                   |                                                  |

A `for` expression is evaluated as follows:

1. If the `for` expression uses multiple variables, it is first expanded to a set of nested `for` expressions, each of which uses only one variable. For example, the expression `for $x in X, $y in Y return $x + $y` is expanded to `for $x in X return for $y in Y return $x + $y`.
2. In a single-variable `for` expression, the variable is called the **range variable**, the value of the expression that follows the `in` keyword is called the **binding sequence**, and the expression that follows the `return` keyword is called the **return expression**. The result of the `for` expression is obtained by evaluating the `return` expression once for each item in the binding sequence, with the range variable bound to that item. The resulting sequences are concatenated (as if by the comma operator) in the order of the items in the binding sequence from which they were derived.

The following example illustrates the use of a `for` expression in restructuring an input document. The example is based on the following input:

```
<bib>
  <book>
    <title>TCP/IP Illustrated</title>
    <author>Stevens</author>
    <publisher>Addison-Wesley</publisher>
  </book>
  <book>
    <title>Advanced Programming in the Unix Environment</title>
    <author>Stevens</author>
    <publisher>Addison-Wesley</publisher>
  </book>
  <book>
    <title>Data on the Web</title>
    <author>Abiteboul</author>
    <author>Buneman</author>
    <author>Suciu</author>
  </book>
</bib>
```

The following example transforms the input document into a list in which each author's name appears only once, followed by a list of titles of books written by that author. This example assumes that the context item is the `bib` element in the input document.

```
for $a in fn:distinct-values(book/author)
return ((book/author[. = $a])[1], book[author = $a]/title)
```

The result of the above expression consists of the following sequence of elements. The titles of books written by a given author are listed after the name of the author. The ordering of `author` elements in the result is implementation-dependent due to the semantics of the `fn:distinct-values` function.

```
<author>Stevens</author>
<title>TCP/IP Illustrated</title>
<title>Advanced Programming in the Unix environment</title>
<author>Abiteboul</author>
<title>Data on the Web</title>
<author>Buneman</author>
<title>Data on the Web</title>
<author>Suciu</author>
<title>Data on the Web</title>
```

The following example illustrates a `for` expression containing more than one variable:

```
for $i in (10, 20),
    $j in (1, 2)
return ($i + $j)
```

The result of the above expression, expressed as a sequence of numbers, is as follows: `11, 12, 21, 22`

The scope of a variable bound in a `for` expression comprises all subexpressions of the `for` expression that appear after the variable binding. The scope does not include the expression to which the variable is bound. The following example illustrates how a variable binding may reference another variable bound earlier in the same `for` expression:

```
for $x in $z, $y in f($x)
return g($x, $y)
```

**Note:**

The focus for evaluation of the `return` clause of a `for` expression is the same as the focus for evaluation of the `for` expression itself. The following example, which attempts to find the total value of a set of order-items, is therefore incorrect:

```
fn:sum(for $i in order-item return @price * @qty)
```

Instead, the expression must be written to use the variable bound in the `for` clause:

```
fn:sum(for $i in order-item return $i/@price * $i/@qty)
```

### 3.10 Let Expressions

XPath allows a variable to be declared and bound to a value using a **let expression**.

| [11]                                             | `LetExpr`                                        | ::=                                              | ` SimpleLetClause "return" ExprSingle `          |                                                  |
| ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ |
| [12]                                             | `SimpleLetClause`                                | ::=                                              | `"let" SimpleLetBinding ("," SimpleLetBinding)*` |                                                  |
| [13]                                             | `SimpleLetBinding`                               | ::=                                              | `"$" VarName ":=" ExprSingle `                   |                                                  |

A let expression is evaluated as follows:

- If the let expression uses multiple variables, it is first expanded to a set of nested let expressions, each of which uses only one variable. For example, the expression `let $x := 4, $y := 3 return $x + $y` is expanded to `let $x := 4 return let $y := 3 return $x + $y`.
- In a single-variable let expression, the variable is called the range variable, the value of the expression that follows the `:=` symbol is called the binding sequence, and the expression that follows the return keyword is called the return expression. The result of the let expression is obtained by evaluating the return expression with the range variable bound to the binding sequence.

The scope of a variable bound in a let expression comprises all subexpressions of the let expression that appear after the variable binding. The scope does not include the expression to which the variable is bound. The following example illustrates how a variable binding may reference another variable bound earlier in the same let expression:

```

let $x := doc('a.xml')/*, $y := $x//*
return $y[@value gt $x/@min]
```

### 3.11 Maps and Arrays

Most modern programming languages have support for collections of key/value pairs, which may be called maps, dictionaries, associative arrays, hash tables, keyed lists, or objects (these are not the same thing as objects in object-oriented systems). In XPath 3.1, we call these maps. Most modern programming languages also support ordered lists of values, which may be called arrays, vectors, or sequences. In XPath 3.1, we have both sequences and arrays. Unlike sequences, an array is an item, and can appear as an item in a sequence.

In previous versions of the language, element structures and sequences were the only complex data structures. We are adding maps and arrays to XPath 3.1 in order to provide lightweight data structures that are easier to optimize and less complex to use for intermediate processing and to allow programs to easily combine XML processing with JSON processing.

**Note:**

The XPath 3.1 specification focuses on syntax provided for maps and arrays, especially constructors and lookup.

Some of the functionality typically needed for maps and arrays is provided by functions defined in [Section 17 Maps and Arrays](https://www.w3.org/TR/xpath-functions-31/#maps-and-arrays)FO31, including functions used to read JSON to create maps and arrays, serialize maps and arrays to JSON, combine maps to create a new map, remove map entries to create a new map, iterate over the keys of a map, convert an array to create a sequence, combine arrays to form a new array, and iterate over arrays in various ways.

#### 3.11.1 Maps

[Definition: A **map** is a function that associates a set of keys with values, resulting in a collection of key / value pairs.] [Definition: Each key / value pair in a map is called an **entry**.] [Definition: The value associated with a given key is called the **associated value** of the key.]

##### 3.11.1.1 Map Constructors

A Map is created using a MapConstructor.

| [69]                                                              | `MapConstructor`                                                  | ::=                                                               | `"map" "{" (MapConstructorEntry ("," MapConstructorEntry)*)? "}"` |                                                                   |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| [70]                                                              | `MapConstructorEntry`                                             | ::=                                                               | ` MapKeyExpr ":" MapValueExpr `                                   |                                                                   |
| [71]                                                              | `MapKeyExpr`                                                      | ::=                                                               | ` ExprSingle `                                                    |                                                                   |
| [72]                                                              | `MapValueExpr`                                                    | ::=                                                               | ` ExprSingle `                                                    |                                                                   |

**Note:**

In some circumstances, it is necessary to include whitespace before or after the colon of a MapConstructorEntry to ensure that it is parsed as intended.

For instance, consider the expression `map{a:b}`. Although it matches the EBNF for MapConstructor (with `a` matching MapKeyExpr and `b` matching MapValueExpr), the "longest possible match" rule requires that `a:b` be parsed as a QName, which results in a syntax error. Changing the expression to `map{a :b}` or `map{a: b}` will prevent this, resulting in the intended parse.

Similarly, consider these three expressions:

```

    map{a:b:c}
    map{a:*:c}
    map{*:b:c}
```

In each case, the expression matches the EBNF in two different ways, but the "longest possible match" rule forces the parse in which the MapKeyExpr is `a:b`, `a:*`, or `*:b` (respectively) and the MapValueExpr is `c`. To achieve the alternative parse (in which the MapKeyExpr is merely `a` or `*`), insert whitespace before and/or after the first colon.

See **A.2 Lexical structure**.

The value of the expression is a map whose entries correspond to the key-value pairs obtained by evaluating the successive MapKeyExpr and MapValueExpr expressions.

Each MapKeyExpr expression is evaluated and atomized; a type error [err:XPTY0004] occurs if the result is not a single atomic value. The associated value is the result of evaluating the corresponding MapValueExpr. If the MapValueExpr evaluates to a node, the associated value is the node itself, not a new node with the same values.

**Note:**

XPath 3.1 has no operators that can distinguish a map or array from another map or array with the same values. Future versions of the XQuery Update Facility, on the other hand, will expose this difference, and need to be clear about the data model instance that is constructed.

In some existing implementations that support updates via proprietary extensions, if the MapValueExpr evaluates to a map or array, the associated value is a new map or array with the same values.

[Definition: Two atomic values `K1` and `K2` have the **same key value** if `op:same-key(K1, K2)` returns `true`, as specified in [Section 17.1.1 op:same-key](https://www.w3.org/TR/xpath-functions-31/#func-same-key)FO31 ] If two or more entries have the same key value then a dynamic error is raised [err:XQDY0137].

Example:

The following expression constructs a map with seven entries:

```

map {
  "Su" : "Sunday",
  "Mo" : "Monday",
  "Tu" : "Tuesday",
  "We" : "Wednesday",
  "Th" : "Thursday",
  "Fr" : "Friday",
  "Sa" : "Saturday"
}
```

Maps can nest, and can contain any XDM value. Here is an example of a nested map with values that can be string values, numeric values, or arrays:

```

map {
    "book": map {
        "title": "Data on the Web",
        "year": 2000,
        "author": [
            map {
                "last": "Abiteboul",
                "first": "Serge"
            },
            map {
                "last": "Buneman",
                "first": "Peter"
            },
            map {
                "last": "Suciu",
                "first": "Dan"
            }
        ],
        "publisher": "Morgan Kaufmann Publishers",
        "price": 39.95
    }
}
```

##### 3.11.1.2 Map Lookup using Function Call Syntax

Maps are functions, and function calls can be used to look up the value associated with a key in a map. If `$map` is a map and `$key` is a key, then `$map($key)` is equivalent to `map:get($map, $key)`. The semantics of such a function call are formally defined in [Section 17.1.6 map:get](https://www.w3.org/TR/xpath-functions-31/#func-map-get)FO31.

Examples:

- `$weekdays("Su")` returns the associated value of the key `Su`.
- `$books("Green Eggs and Ham")` returns associated value of the key `Green Eggs and Ham`.

**Note:**

XPath 3.1 also provides an alternate syntax for map and array lookup that is more terse, supports wildcards, and allows lookup to iterate over a sequence of maps or arrays. See **3.11.3 The Lookup Operator ("?") for Maps and Arrays** for details.

Map lookups can be chained.

Examples: (These examples assume that `$b` is bound to the books map from the previous section)

- The expression `$b("book")("title")` returns the string `Data on the Web`.
- The expression `$b("book")("author")` returns the array of authors.
- The expression `$b("book")("author")(1)("last")` returns the string `Abiteboul`. (This example combines **3.11.2.2 Array Lookup using Function Call Syntax** with map lookups.)

#### 3.11.2 Arrays

##### 3.11.2.1 Array Constructors

[Definition: An **array** is a function that associates a set of positions, represented as positive integer keys, with values.] The first position in an array is associated with the integer 1. [Definition: The values of an array are called its **members**.] In the type hierarchy, array has a distinct type, which is derived from function. Atomization converts arrays to sequences (see Atomization).

An array is created using an ArrayConstructor.

| [73]                                                | `ArrayConstructor`                                  | ::=                                                 | ` SquareArrayConstructor \| CurlyArrayConstructor ` |                                                     |
| --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- |
| [74]                                                | `SquareArrayConstructor`                            | ::=                                                 | `"[" (ExprSingle ("," ExprSingle)*)? "]"`           |                                                     |
| [75]                                                | `CurlyArrayConstructor`                             | ::=                                                 | `"array" EnclosedExpr `                             |                                                     |

If a member of an array is a node, its node identity is preserved. In both forms of an ArrayConstructor, if a member expression evaluates to a node, the associated value is the node itself, not a new node with the same values. If the member expression evaluates to a map or array, the associated value is a new map or array with the same values.

A SquareArrayConstructor consists of a comma-delimited set of argument expressions. It returns an array in which each member contains the value of the corresponding argument expression.

Examples:

- `[ 1, 2, 5, 7 ]` creates an array with four members: `1`, `2`, `5`, and `7`.
- `[ (), (27, 17, 0)]` creates an array with two members: `()` and the sequence `(27, 17, 0)`.
- `[ $x, local:items(), <tautology>It is what it is.</tautology> ]` creates an array with three members: the value of $x, the result of evaluating the function call, and a tautology element.

A CurlyArrayConstructor can use any expression to create its members. It evaluates its operand expression to obtain a sequence of items and creates an array with these items as members. Unlike a SquareArrayConstructor, a comma in a CurlyArrayConstructor is the comma operator, not a delimiter.

Examples:

- `array { $x }` creates an array with one member for each item in the sequence to which $x is bound.
- `array { local:items() }` creates an array with one member for each item in the sequence to which `local:items()` evaluates.
- `array { 1, 2, 5, 7 }` creates an array with four members: `1`, `2`, `5`, and `7`.
- `array { (), (27, 17, 0) }` creates an array with three members: `27`, `17`, and `0`.
- `array{ $x, local:items(), <tautology>It is what it is.</tautology> }` creates an array with the following members: the items to which `$x` is bound, followed by the items to which `local:items()` evaluates, followed by a tautology element.

**Note:**

XPath 3.1 does not provide explicit support for sparse arrays. Use integer-valued maps to represent sparse arrays, e.g. `map { 27 : -1, 153 : 17 } `.

##### 3.11.2.2 Array Lookup using Function Call Syntax

Arrays are functions, and function calls can be used to look up the value associated with position in an array. If `$array` is an array and `$index` is an integer corresponding to a position in the array, then `$array($key)` is equivalent to `array:get($array, $key)`. The semantics of such a function call are formally defined in [Section 17.3.2 array:get](https://www.w3.org/TR/xpath-functions-31/#func-array-get)FO31.

Examples:

- `[ 1, 2, 5, 7 ](4)` evaluates to `7`.
- `[ [1, 2, 3], [4, 5, 6]](2)` evaluates to `[4, 5, 6]`.
- `[ [1, 2, 3], [4, 5, 6]](2)(2)` evaluates to `5`.
- `[ 'a', 123, <name>Robert Johnson</name> ](3)` evaluates to `<name>Robert Johnson</name>`.
- `array { (), (27, 17, 0) }(1)` evaluates to `27`.
- `array { (), (27, 17, 0) }(2)` evaluates to `17`.
- `array { "licorice", "ginger" }(20)` raises a dynamic error [[err:FOAY0001](https://www.w3.org/TR/xpath-functions-31/#ERRFOAY0001)]FO31.

**Note:**

XPath 3.1 also provides an alternate syntax for map and array lookup that is more terse, supports wildcards, and allows lookup to iterate over a sequence of maps or arrays. See **3.11.3 The Lookup Operator ("?") for Maps and Arrays** for details.

#### 3.11.3 The Lookup Operator ("?") for Maps and Arrays

XPath 3.1 provides a lookup operator for maps and arrays that is more convenient for some common cases. It provides a terse syntax for simple strings as keys in maps or integers as keys in arrays, supports wildcards, and iterates over sequences of maps and arrays.

##### 3.11.3.1 Unary Lookup

| [76]                                                    | `UnaryLookup`                                           | ::=                                                     | `"?" KeySpecifier `                                     |                                                         |
| ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| [54]                                                    | `KeySpecifier`                                          | ::=                                                     | ` NCName \| IntegerLiteral \| ParenthesizedExpr \| "*"` |                                                         |

Unary lookup is used in predicates (e.g. `$map[?name='Mike']` or with the simple map operator (e.g. `$maps ! ?name='Mike'`). See **3.11.3.2 Postfix Lookup** for the postfix lookup operator.

UnaryLookup returns a sequence of values selected from the context item, which must be a map or array. If the context item is not a map or an array, a type error is raised [err:XPTY0004].

If the context item is a map:

1. If the KeySpecifier is an `NCName`, the UnaryLookup operator is equivalent to `.(KS)`, where `KS` is the value of the `NCName`.
2. If the KeySpecifier is an IntegerLiteral, the UnaryLookup operator is equivalent to `.(KS)`, where `KS` is the value of the IntegerLiteral.
3. If the KeySpecifier is a ParenthesizedExpr, the UnaryLookup operator is equivalent to the following expression, where `KS` is the value of the ParenthesizedExpr: for $k in fn:data(KS) return .($k)
4. If the KeySpecifier is a wildcard ("`*`"), the UnaryLookup operator is equivalent to the following expression: for $k in map:keys(.) return .($k) **Note:** The order of keys in map:keys() is implementation-dependent, so the order of values in the result sequence is also implementation-dependent.

If the context item is an array:

1. If the KeySpecifier is an IntegerLiteral, the UnaryLookup operator is equivalent to `.(KS)`, where `KS` is the value of the IntegerLiteral.
2. If the KeySpecifier is an `NCName`, the UnaryLookup operator raises a type error [err:XPTY0004].
3. If the KeySpecifier is a ParenthesizedExpr, the UnaryLookup operator is equivalent to the following expression, where `KS` is the value of the ParenthesizedExpr: for $k in fn:data(KS) return .($k)
4. If the KeySpecifier is a wildcard ("`*`"), the UnaryLookup operator is equivalent to the following expression: for $k in 1 to array:size(.) return .($k) **Note:** Note that array items are returned in order.

Examples:

- `?name` is equivalent to `.("name")`, an appropriate lookup for a map.
- `?2` is equivalent to `.(2)`, an appropriate lookup for an array or an integer-valued map.
- `?($a)` is equivalent to `for $k in $a return .($k)`, allowing keys for an array or map to be passed using a variable.
- `?(2 to 4)` is equivalent to `for $k in (2,3,4) return .($k)`, a convenient way to return a range of values from an array.
- `?(3.5)` raises a type error if the context item is an array because the parameter must be an integer.
- `([1,2,3], [1,2,5], [1,2])[?3 = 5]` raises an error because `?3` on one of the items in the sequence fails.
- If `$m` is bound to the weekdays map described in **3.11.1 Maps**, then `$m?*` returns the values `("Sunday","Monday","Tuesday","Wednesday", "Thursday", "Friday","Saturday")`, in implementation-dependent order.
- `[1, 2, 5, 7]?*` evaluates to `(1, 2, 5, 7)`.
- `[[1, 2, 3], [4, 5, 6]]?*` evaluates to `([1, 2, 3], [4, 5, 6])`

##### 3.11.3.2 Postfix Lookup

| [53]                | `Lookup`            | ::=                 | `"?" KeySpecifier ` |                     |
| ------------------- | ------------------- | ------------------- | ------------------- | ------------------- |

The semantics of a Postfix Lookup expression depend on the form of the KeySpecifier, as follows:

- If the `KeySpecifier` is an `NCName`, `IntegerLiteral`, or `Wildcard` ("`*`"), then the expression `E?S` is equivalent to `E!?S`. (That is, the semantics of the postfix lookup operator are defined in terms of the unary lookup operator).
- If the `KeySpecifier` is a `ParenthesizedExpr`, then the expression `E?(S)` is equivalent to for $e in E, $s in fn:data(S) return $e($s) **Note:** The focus for evaluating `S` is the same as the focus for the `Lookup` expression itself.

Examples:

- `map { "first" : "Jenna", "last" : "Scott" }?first` evaluates to `"Jenna"`
- `[4, 5, 6]?2` evaluates to `5`.
- `(map {"first": "Tom"}, map {"first": "Dick"}, map {"first": "Harry"})?first` evaluates to the sequence `("Tom", "Dick", "Harry")` .
- `([1,2,3], [4,5,6])?2` evaluates to the sequence `(2, 5)`.
- `["a","b"]?3` raises a dynamic error [[err:FOAY0001](https://www.w3.org/TR/xpath-functions-31/#ERRFOAY0001)]FO31

### 3.12 Conditional Expressions

XPath 3.1 supports a conditional expression based on the keywords `if`, `then`, and `else`.

| [15]                                                     | `IfExpr`                                                 | ::=                                                      | `"if" "(" Expr ")" "then" ExprSingle "else" ExprSingle ` |                                                          |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |

The expression following the `if` keyword is called the **test expression**, and the expressions following the `then` and `else` keywords are called the **then-expression** and **else-expression**, respectively.

The first step in processing a conditional expression is to find the effective boolean value of the test expression, as defined in **2.4.3 Effective Boolean Value**.

The value of a conditional expression is defined as follows: If the effective boolean value of the test expression is `true`, the value of the then-expression is returned. If the effective boolean value of the test expression is `false`, the value of the else-expression is returned.

Conditional expressions have a special rule for propagating dynamic errors. If the effective value of the test expression is `true`, the conditional expression ignores (does not raise) any dynamic errors encountered in the else-expression. In this case, since the else-expression can have no observable effect, it need not be evaluated. Similarly, if the effective value of the test expression is `false`, the conditional expression ignores any dynamic errors encountered in the then-expression, and the then-expression need not be evaluated.

Here are some examples of conditional expressions:

- In this example, the test expression is a comparison expression: if ($widget1/unit-cost < $widget2/unit-cost) then $widget1 else $widget2
- In this example, the test expression tests for the existence of an attribute named `discounted`, independently of its value: if ($part/@discounted) then $part/wholesale else $part/retail

### 3.13 Quantified Expressions

Quantified expressions support existential and universal quantification. The value of a quantified expression is always `true` or `false`.

| [14]                                                                             | `QuantifiedExpr`                                                                 | ::=                                                                              | `("some" \| "every") "$" VarName "in" ExprSingle ("," "$" VarName "in" ExprSingl |                                                                                  |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |

A **quantified expression** begins with a **quantifier**, which is the keyword `some` or `every`, followed by one or more in-clauses that are used to bind variables, followed by the keyword `satisfies` and a test expression. Each in-clause associates a variable with an expression that returns a sequence of items, called the binding sequence for that variable. The in-clauses generate tuples of variable bindings, including a tuple for each combination of items in the binding sequences of the respective variables. Conceptually, the test expression is evaluated for each tuple of variable bindings. Results depend on the effective boolean value of the test expressions, as defined in **2.4.3 Effective Boolean Value**. The value of the quantified expression is defined by the following rules:

1. If the quantifier is `some`, the quantified expression is `true` if at least one evaluation of the test expression has the effective boolean value `true`; otherwise the quantified expression is `false`. This rule implies that, if the in-clauses generate zero binding tuples, the value of the quantified expression is `false`.
2. If the quantifier is `every`, the quantified expression is `true` if every evaluation of the test expression has the effective boolean value `true`; otherwise the quantified expression is `false`. This rule implies that, if the in-clauses generate zero binding tuples, the value of the quantified expression is `true`.

The scope of a variable bound in a quantified expression comprises all subexpressions of the quantified expression that appear after the variable binding. The scope does not include the expression to which the variable is bound.

The order in which test expressions are evaluated for the various binding tuples is implementation-dependent. If the quantifier is `some`, an implementation may return `true` as soon as it finds one binding tuple for which the test expression has an effective boolean value of `true`, and it may raise a dynamic error as soon as it finds one binding tuple for which the test expression raises an error. Similarly, if the quantifier is `every`, an implementation may return `false` as soon as it finds one binding tuple for which the test expression has an effective boolean value of `false`, and it may raise a dynamic error as soon as it finds one binding tuple for which the test expression raises an error. As a result of these rules, the value of a quantified expression is not deterministic in the presence of errors, as illustrated in the examples below.

Here are some examples of quantified expressions:

- This expression is `true` if every `part` element has a `discounted` attribute (regardless of the values of these attributes): every $part in /parts/part satisfies $part/@discounted
- This expression is `true` if at least one `employee` element satisfies the given comparison expression: some $emp in /emps/employee satisfies ($emp/bonus > 0.25 * $emp/salary)
- In the following examples, each quantified expression evaluates its test expression over nine tuples of variable bindings, formed from the Cartesian product of the sequences `(1, 2, 3)` and `(2, 3, 4)`. The expression beginning with `some` evaluates to `true`, and the expression beginning with `every` evaluates to `false`. some $x in (1, 2, 3), $y in (2, 3, 4) satisfies $x + $y = 4 every $x in (1, 2, 3), $y in (2, 3, 4) satisfies $x + $y = 4
- This quantified expression may either return `true` or raise a type error, since its test expression returns `true` for one variable binding and raises a type error for another: some $x in (1, 2, "cat") satisfies $x * 2 = 4
- This quantified expression may either return `false` or raise a type error, since its test expression returns `false` for one variable binding and raises a type error for another: every $x in (1, 2, "cat") satisfies $x * 2 = 4

### 3.14 Expressions on SequenceTypes

The `instance of`, `cast`, `castable`, and `treat` expressions are used to test whether a value conforms to a given type or to convert it to an instance of a given type.

#### 3.14.1 Instance Of

| [25]                                           | `InstanceofExpr`                               | ::=                                            | ` TreatExpr ( "instance" "of" SequenceType )?` |                                                |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |

The boolean operator `instance of` returns `true` if the value of its first operand matches the SequenceType in its second operand, according to the rules for SequenceType matching; otherwise it returns `false`. For example:

- `5 instance of xs:integer` This example returns `true` because the given value is an instance of the given type.
- `5 instance of xs:decimal` This example returns `true` because the given value is an integer literal, and `xs:integer` is derived by restriction from `xs:decimal`.
- `(5, 6) instance of xs:integer+` This example returns `true` because the given sequence contains two integers, and is a valid instance of the specified type.
- `. instance of element()` This example returns `true` if the context item is an element node or `false` if the context item is defined but is not an element node. If the context item is [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31, a dynamic error is raised [err:XPDY0002].

#### 3.14.2 Cast

| [28]                                     | `CastExpr`                               | ::=                                      | ` ArrowExpr ( "cast" "as" SingleType )?` |                                          |
| ---------------------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| [77]                                     | `SingleType`                             | ::=                                      | ` SimpleTypeName "?"?`                   |                                          |

Occasionally it is necessary to convert a value to a specific datatype. For this purpose, XPath 3.1 provides a `cast` expression that creates a new value of a specific type based on an existing value. A `cast` expression takes two operands: an **input expression** and a **target type**. The type of the atomized value of the input expression is called the **input type**. The SimpleTypeName must be the name of a type defined in the in-scope schema types, and it must be a simple type [err:XQST0052]. In addition, the target type cannot be `xs:NOTATION`, `xs:anySimpleType`, or `xs:anyAtomicType` [err:XPST0080]. The optional occurrence indicator "`?`" denotes that an empty sequence is permitted. If the target type is a lexical QName that has no namespace prefix, it is considered to be in the default element/type namespace.

Casting a node to `xs:QName` can cause surprises because it uses the static context of the cast expression to provide the namespace bindings for this operation. Instead of casting to `xs:QName`, it is generally preferable to use the `fn:QName` function, which allows the namespace context to be taken from the document containing the QName.

The semantics of the `cast` expression are as follows:

1. The input expression is evaluated.
2. The result of the first step is atomized.
3. If the result of atomization is a sequence of more than one atomic value, a type error is raised [err:XPTY0004].
4. If the result of atomization is an empty sequence: If `?` is specified after the target type, the result of the `cast` expression is an empty sequence. If `?` is not specified after the target type, a type error is raised [err:XPTY0004].
5. If the result of atomization is a single atomic value, the result of the cast expression is determined by casting to the target type as described in [Section 19 Casting](https://www.w3.org/TR/xpath-functions-31/#casting)FO31. When casting, an implementation may need to determine whether one type is derived by restriction from another. An implementation can determine this either by examining the in-scope schema definitions or by using an alternative, implementation-dependent mechanism such as a data dictionary. The result of a cast expression is one of the following: A value of the target type (or, in the case of list types, a sequence of values that are instances of the item type of the list type). A type error, if casting from the source type to the target type is not supported (for example attempting to convert an integer to a date). A dynamic error, if the particular input value cannot be converted to the target type (for example, attempting to convert the string `"three"` to an integer).

#### 3.14.3 Castable

| [27]                                        | `CastableExpr`                              | ::=                                         | ` CastExpr ( "castable" "as" SingleType )?` |                                             |
| ------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ------------------------------------------- |
| [77]                                        | `SingleType`                                | ::=                                         | ` SimpleTypeName "?"?`                      |                                             |

XPath 3.1 provides an expression that tests whether a given value is castable into a given target type. The SimpleTypeName must be the name of a type defined in the in-scope schema types, and the type must be `simple` [err:XQST0052]. In addition, the target type cannot be `xs:NOTATION`, `xs:anySimpleType`, or `xs:anyAtomicType` [err:XPST0080]. The optional occurrence indicator "`?`" denotes that an empty sequence is permitted.

The expression `E castable as T` returns `true` if the result of evaluating `E` can be successfully cast into the target type `T` by using a `cast` expression; otherwise it returns `false`. If evaluation of `E` fails with a dynamic error or if the value of `E` cannot be atomized, the `castable` expression as a whole fails. The `castable` expression can be used as a predicate to avoid errors at evaluation time. It can also be used to select an appropriate type for processing of a given value, as illustrated in the following example:

```

if ($x castable as hatsize)
   then $x cast as hatsize
   else if ($x castable as IQ)
   then $x cast as IQ
   else $x cast as xs:string
```

#### 3.14.4 Constructor Functions

For every simple type in the in-scope schema types (except `xs:NOTATION` and `xs:anyAtomicType`, and `xs:anySimpleType`, which are not instantiable), a **constructor function** is implicitly defined. In each case, the name of the constructor function is the same as the name of its target type (including namespace). The signature of the constructor function for a given type depends on the type that is being constructed, and can be found in [Section 18 Constructor functions](https://www.w3.org/TR/xpath-functions-31/#constructor-functions)FO31.

[Definition: The **constructor function** for a given type is used to convert instances of other simple types into the given type. The semantics of the constructor function call `T($arg)` are defined to be equivalent to the expression `(($arg) cast as T?)`.]

The following examples illustrate the use of constructor functions:

- This example is equivalent to `("2000-01-01" cast as xs:date?)`. xs:date("2000-01-01")
- This example is equivalent to `(($floatvalue * 0.2E-5) cast as xs:decimal?)`. xs:decimal($floatvalue * 0.2E-5)
- This example returns an `xs:dayTimeDuration` value equal to 21 days. It is equivalent to `("P21D" cast as xs:dayTimeDuration?)`. xs:dayTimeDuration("P21D")
- If `usa:zipcode` is a user-defined atomic type in the in-scope schema types, then the following expression is equivalent to the expression `("12345" cast as usa:zipcode?)`. usa:zipcode("12345")

**Note:**

An instance of an atomic type that is not in a namespace can be constructed by using a URIQualifiedName in either a cast expression or a constructor function call. Examples:

```
17 cast as Q{}apple
```

```
Q{}apple(17)
```

If the default element/type namespace is absent, the QName syntax can also be used. Examples:

```
17 cast as apple
```

```
apple(17)
```

#### 3.14.5 Treat

| [26]                                           | `TreatExpr`                                    | ::=                                            | ` CastableExpr ( "treat" "as" SequenceType )?` |                                                |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |

XPath 3.1 provides an expression called `treat` that can be used to modify the static type of its operand.

Like `cast`, the `treat` expression takes two operands: an expression and a SequenceType. Unlike `cast`, however, `treat` does not change the dynamic type or value of its operand. Instead, the purpose of `treat` is to ensure that an expression has an expected dynamic type at evaluation time.

The semantics of *`expr1`* ` treat as ` *`type1`* are as follows:

- During static analysis: The static type of the `treat` expression is *`type1`*. This enables the expression to be used as an argument of a function that requires a parameter of *`type1`*.
- During expression evaluation: If *`expr1`* matches *`type1`*, using the rules for SequenceType matching, the `treat` expression returns the value of *`expr1`*; otherwise, it raises a dynamic error [err:XPDY0050]. If the value of *`expr1`* is returned, the identity of any nodes in the value is preserved. The `treat` expression ensures that the value of its expression operand conforms to the expected type at run-time.
- Example: $myaddress treat as element(*, USAddress) The static type of `$myaddress` may be `element(*, Address)`, a less specific type than `element(*, USAddress)`. However, at run-time, the value of `$myaddress` must match the type `element(*, USAddress)` using rules for SequenceType matching; otherwise a dynamic error is raised [err:XPDY0050].

### 3.15 Simple map operator (`!`)

| [35]                        | `SimpleMapExpr`             | ::=                         | ` PathExpr ("!" PathExpr)*` |                             |
| --------------------------- | --------------------------- | --------------------------- | --------------------------- | --------------------------- |

A mapping expression `S!E` evaluates the expression `E` once for every item in the sequence obtained by evaluating `S`. The simple mapping operator "`!`" can be applied to any sequence, regardless of the types of its items, and it can deliver a mixed sequence of nodes, atomic values, and functions. Unlike the similar "`/`" operator, it does not sort nodes into document order or eliminate duplicates.

Each operation `E1!E2` is evaluated as follows: Expression `E1` is evaluated to a sequence `S`. Each item in `S` then serves in turn to provide an inner focus (the item as the context item, its position in `S` as the context position, the length of `S` as the context size) for an evaluation of `E2` in the dynamic context. The sequences resulting from all the evaluations of `E2` are combined as follows: Every evaluation of `E2` returns a (possibly empty) sequence of items. These sequences are concatenated and returned. The returned sequence preserves the orderings within and among the subsequences generated by the evaluations of `E2` .

Simple map operators have functionality similar to **3.3.1.1 Path operator (/)**. The following table summarizes the differences between these two operators
| Operator                                                   | Path operator (`E1 / E2`)                                  | Simple map operator (`E1 ! E2`)                            |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| E1                                                         | Any sequence of nodes                                      | Any sequence of items                                      |
| E2                                                         | Either a sequence of nodes or a sequence of non-node items | A sequence of items                                        |
| Additional processing                                      | Duplicate elimination and document ordering                | Simple sequence concatenation                              |

The following examples illustrate the use of simple map operators combined with path expressions.

- `child::div1 / child::para / string() ! concat("id-", .)` Selects the `para` element children of the `div1` element children of the context node; that is, the `para` element grandchildren of the context node that have `div1` parents. It then outputs the strings obtained by prepending `"id-"` to each of the string values of these grandchildren.
- `$emp ! (@first, @middle, @last)` Returns the values of the attributes `first`, `middle`, and `last` for element `$emp`, in the order given. (The `/` operator here returns the attributes in an unpredictable order.)
- `$docs ! ( //employee)` Returns all the employees within all the documents identified by the variable docs, in document order within each document, but retaining the order of documents.
- `avg( //employee / salary ! translate(., '$', '') ! number(.))` Returns the average salary of the employees, having converted the salary to a number by removing any `$` sign and then converting to a number. (The second occurrence of `!` could not be written as `/` because the left-hand operand of `/` cannot be an atomic value.)
- `fn:string-join((1 to $n)!"*")` Returns a string containing `$n` asterisks.
- `$values!(.*.) => fn:sum()` Returns the sum of the squares of a sequence of numbers.
- `string-join(ancestor::*!name(), '/')` Returns a path containing the names of the ancestors of an element, separated by "`/`" characters.

### 3.16 Arrow operator (`=>`)

| [29]                                                       | `ArrowExpr`                                                | ::=                                                        | ` UnaryExpr ( "=>" ArrowFunctionSpecifier ArgumentList )*` |                                                            |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| [55]                                                       | `ArrowFunctionSpecifier`                                   | ::=                                                        | ` EQName \| VarRef \| ParenthesizedExpr `                  |                                                            |

[Definition: An **arrow operator** applies a function to the value of an expression, using the value as the first argument to the function.] Given a UnaryExpr `U`, an ArrowFunctionSpecifier `F`, and an ArgumentList `(A, B, C...)`, the expression `U => F(A, B, C...)` is equivalent to the expression `F(U, A, B, C...)`.

This syntax is particularly helpful when applying multiple functions to a value in turn. For example, the following expression invites syntax errors due to misplaced parentheses:

```
tokenize((normalize-unicode(upper-case($string))),"\s+")
```

In the following reformulation, it is easier to see that the parentheses are balanced:

```
$string => upper-case() => normalize-unicode() => tokenize("\s+")
```

## 4 Conformance

This section defines the conformance criteria for an XPath 3.1 processor. In this section, the following terms are used to indicate the requirement levels defined in [RFC2119]. [Definition: **MUST** means that the item is an absolute requirement of the specification.] [Definition: **MUST NOT** means that the item is an absolute prohibition of the specification.] [Definition: **MAY** means that an item is truly optional.]

XPath is intended primarily as a component that can be used by other specifications. Therefore, XPath relies on specifications that use it (such as [XPointer] and [XSL Transformations (XSLT) Version 3.0]) to specify conformance criteria for XPath in their respective environments. Specifications that set conformance criteria for their use of XPath MUST NOT change the syntactic or semantic definitions of XPath as given in this specification, except by subsetting and/or compatible extensions.

If a language is described as an extension of XPath, then every expression that conforms to the XPath grammar MUST behave as described in this specification.

### 4.1 Static Typing Feature

[Definition: The **Static Typing Feature** is an optional feature of XPath that provides support for static semantics, and requires implementations to detect and report type errors during the static analysis phase.] Specifications that use XPath MAY specify conformance criteria for use of the Static Typing Feature.

If an implementation does not support the Static Typing Feature, but can nevertheless determine during the static analysis phase that an XPath expression, if evaluated, would necessarily raise a dynamic error or that an expression, if evaluated, would necessarily raise a type error, the implementation MAY raise that error during the static analysis phase. The choice of whether to raise such an error at analysis time is implementation dependent.

## A XPath 3.1 Grammar

### A.1 EBNF

The grammar of XPath 3.1 uses the same simple Extended Backus-Naur Form (EBNF) notation as [XML 1.0] with the following minor differences.

- All named symbols have a name that begins with an uppercase letter.
- It adds a notation for referring to productions in external specifications.
- Comments or extra-grammatical constraints on grammar productions are between '/*' and '*/' symbols. A 'xgc:' prefix is an extra-grammatical constraint, the details of which are explained in **A.1.2 Extra-grammatical Constraints** A 'ws:' prefix explains the whitespace rules for the production, the details of which are explained in **A.2.4 Whitespace Rules** A 'gn:' prefix means a 'Grammar Note', and is meant as a clarification for parsing rules, and is explained in **A.1.3 Grammar Notes**. These notes are not normative.

The terminal symbols for this grammar include the quoted strings used in the production rules below, and the terminal symbols defined in section **A.2.1 Terminal Symbols**.

The EBNF notation is described in more detail in **A.1.1 Notation**.

| [1]                                                                              | `XPath`                                                                          | ::=                                                                              | ` Expr `                                                                         |                                                                                  |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [2]                                                                              | `ParamList`                                                                      | ::=                                                                              | ` Param ("," Param)*`                                                            |                                                                                  |
| [3]                                                                              | `Param`                                                                          | ::=                                                                              | `"$" EQName TypeDeclaration?`                                                    |                                                                                  |
| [4]                                                                              | `FunctionBody`                                                                   | ::=                                                                              | ` EnclosedExpr `                                                                 |                                                                                  |
| [5]                                                                              | `EnclosedExpr`                                                                   | ::=                                                                              | `"{" Expr? "}"`                                                                  |                                                                                  |
| [6]                                                                              | `Expr`                                                                           | ::=                                                                              | ` ExprSingle ("," ExprSingle)*`                                                  |                                                                                  |
| [7]                                                                              | `ExprSingle`                                                                     | ::=                                                                              | ` ForExpr \| LetExpr \| QuantifiedExpr \| IfExpr \| OrExpr `                     |                                                                                  |
| [8]                                                                              | `ForExpr`                                                                        | ::=                                                                              | ` SimpleForClause "return" ExprSingle `                                          |                                                                                  |
| [9]                                                                              | `SimpleForClause`                                                                | ::=                                                                              | `"for" SimpleForBinding ("," SimpleForBinding)*`                                 |                                                                                  |
| [10]                                                                             | `SimpleForBinding`                                                               | ::=                                                                              | `"$" VarName "in" ExprSingle `                                                   |                                                                                  |
| [11]                                                                             | `LetExpr`                                                                        | ::=                                                                              | ` SimpleLetClause "return" ExprSingle `                                          |                                                                                  |
| [12]                                                                             | `SimpleLetClause`                                                                | ::=                                                                              | `"let" SimpleLetBinding ("," SimpleLetBinding)*`                                 |                                                                                  |
| [13]                                                                             | `SimpleLetBinding`                                                               | ::=                                                                              | `"$" VarName ":=" ExprSingle `                                                   |                                                                                  |
| [14]                                                                             | `QuantifiedExpr`                                                                 | ::=                                                                              | `("some" \| "every") "$" VarName "in" ExprSingle ("," "$" VarName "in" ExprSingl |                                                                                  |
| [15]                                                                             | `IfExpr`                                                                         | ::=                                                                              | `"if" "(" Expr ")" "then" ExprSingle "else" ExprSingle `                         |                                                                                  |
| [16]                                                                             | `OrExpr`                                                                         | ::=                                                                              | ` AndExpr ( "or" AndExpr )*`                                                     |                                                                                  |
| [17]                                                                             | `AndExpr`                                                                        | ::=                                                                              | ` ComparisonExpr ( "and" ComparisonExpr )*`                                      |                                                                                  |
| [18]                                                                             | `ComparisonExpr`                                                                 | ::=                                                                              | ` StringConcatExpr ( (ValueComp \| GeneralComp \| NodeComp) StringConcatExpr )?` |                                                                                  |
| [19]                                                                             | `StringConcatExpr`                                                               | ::=                                                                              | ` RangeExpr ( "\|\|" RangeExpr )*`                                               |                                                                                  |
| [20]                                                                             | `RangeExpr`                                                                      | ::=                                                                              | ` AdditiveExpr ( "to" AdditiveExpr )?`                                           |                                                                                  |
| [21]                                                                             | `AdditiveExpr`                                                                   | ::=                                                                              | ` MultiplicativeExpr ( ("+" \| "-") MultiplicativeExpr )*`                       |                                                                                  |
| [22]                                                                             | `MultiplicativeExpr`                                                             | ::=                                                                              | ` UnionExpr ( ("*" \| "div" \| "idiv" \| "mod") UnionExpr )*`                    |                                                                                  |
| [23]                                                                             | `UnionExpr`                                                                      | ::=                                                                              | ` IntersectExceptExpr ( ("union" \| "\|") IntersectExceptExpr )*`                |                                                                                  |
| [24]                                                                             | `IntersectExceptExpr`                                                            | ::=                                                                              | ` InstanceofExpr ( ("intersect" \| "except") InstanceofExpr )*`                  |                                                                                  |
| [25]                                                                             | `InstanceofExpr`                                                                 | ::=                                                                              | ` TreatExpr ( "instance" "of" SequenceType )?`                                   |                                                                                  |
| [26]                                                                             | `TreatExpr`                                                                      | ::=                                                                              | ` CastableExpr ( "treat" "as" SequenceType )?`                                   |                                                                                  |
| [27]                                                                             | `CastableExpr`                                                                   | ::=                                                                              | ` CastExpr ( "castable" "as" SingleType )?`                                      |                                                                                  |
| [28]                                                                             | `CastExpr`                                                                       | ::=                                                                              | ` ArrowExpr ( "cast" "as" SingleType )?`                                         |                                                                                  |
| [29]                                                                             | `ArrowExpr`                                                                      | ::=                                                                              | ` UnaryExpr ( "=>" ArrowFunctionSpecifier ArgumentList )*`                       |                                                                                  |
| [30]                                                                             | `UnaryExpr`                                                                      | ::=                                                                              | `("-" \| "+")* ValueExpr `                                                       |                                                                                  |
| [31]                                                                             | `ValueExpr`                                                                      | ::=                                                                              | ` SimpleMapExpr `                                                                |                                                                                  |
| [32]                                                                             | `GeneralComp`                                                                    | ::=                                                                              | `"=" \| "!=" \| "<" \| "<=" \| ">" \| ">="`                                      |                                                                                  |
| [33]                                                                             | `ValueComp`                                                                      | ::=                                                                              | `"eq" \| "ne" \| "lt" \| "le" \| "gt" \| "ge"`                                   |                                                                                  |
| [34]                                                                             | `NodeComp`                                                                       | ::=                                                                              | `"is" \| "<<" \| ">>"`                                                           |                                                                                  |
| [35]                                                                             | `SimpleMapExpr`                                                                  | ::=                                                                              | ` PathExpr ("!" PathExpr)*`                                                      |                                                                                  |
| [36]                                                                             | `PathExpr`                                                                       | ::=                                                                              | `("/" RelativePathExpr?)\| ("//" RelativePathExpr)\| RelativePathExpr `          | */* xgc: leading-lone-slash */*                                                  |
| [37]                                                                             | `RelativePathExpr`                                                               | ::=                                                                              | ` StepExpr (("/" \| "//") StepExpr)*`                                            |                                                                                  |
| [38]                                                                             | `StepExpr`                                                                       | ::=                                                                              | ` PostfixExpr \| AxisStep `                                                      |                                                                                  |
| [39]                                                                             | `AxisStep`                                                                       | ::=                                                                              | `(ReverseStep \| ForwardStep) PredicateList `                                    |                                                                                  |
| [40]                                                                             | `ForwardStep`                                                                    | ::=                                                                              | `(ForwardAxis NodeTest) \| AbbrevForwardStep `                                   |                                                                                  |
| [41]                                                                             | `ForwardAxis`                                                                    | ::=                                                                              | `("child" "::")\| ("descendant" "::")\| ("attribute" "::")\| ("self" "::")\| ("d |                                                                                  |
| [42]                                                                             | `AbbrevForwardStep`                                                              | ::=                                                                              | `"@"? NodeTest `                                                                 |                                                                                  |
| [43]                                                                             | `ReverseStep`                                                                    | ::=                                                                              | `(ReverseAxis NodeTest) \| AbbrevReverseStep `                                   |                                                                                  |
| [44]                                                                             | `ReverseAxis`                                                                    | ::=                                                                              | `("parent" "::")\| ("ancestor" "::")\| ("preceding-sibling" "::")\| ("preceding" |                                                                                  |
| [45]                                                                             | `AbbrevReverseStep`                                                              | ::=                                                                              | `".."`                                                                           |                                                                                  |
| [46]                                                                             | `NodeTest`                                                                       | ::=                                                                              | ` KindTest \| NameTest `                                                         |                                                                                  |
| [47]                                                                             | `NameTest`                                                                       | ::=                                                                              | ` EQName \| Wildcard `                                                           |                                                                                  |
| [48]                                                                             | `Wildcard`                                                                       | ::=                                                                              | `"*"\| (NCName ":*")\| ("*:" NCName)\| (BracedURILiteral "*")`                   | */* ws: explicit */*                                                             |
| [49]                                                                             | `PostfixExpr`                                                                    | ::=                                                                              | ` PrimaryExpr (Predicate \| ArgumentList \| Lookup)*`                            |                                                                                  |
| [50]                                                                             | `ArgumentList`                                                                   | ::=                                                                              | `"(" (Argument ("," Argument)*)? ")"`                                            |                                                                                  |
| [51]                                                                             | `PredicateList`                                                                  | ::=                                                                              | ` Predicate*`                                                                    |                                                                                  |
| [52]                                                                             | `Predicate`                                                                      | ::=                                                                              | `"[" Expr "]"`                                                                   |                                                                                  |
| [53]                                                                             | `Lookup`                                                                         | ::=                                                                              | `"?" KeySpecifier `                                                              |                                                                                  |
| [54]                                                                             | `KeySpecifier`                                                                   | ::=                                                                              | ` NCName \| IntegerLiteral \| ParenthesizedExpr \| "*"`                          |                                                                                  |
| [55]                                                                             | `ArrowFunctionSpecifier`                                                         | ::=                                                                              | ` EQName \| VarRef \| ParenthesizedExpr `                                        |                                                                                  |
| [56]                                                                             | `PrimaryExpr`                                                                    | ::=                                                                              | ` Literal \| VarRef \| ParenthesizedExpr \| ContextItemExpr \| FunctionCall \| F |                                                                                  |
| [57]                                                                             | `Literal`                                                                        | ::=                                                                              | ` NumericLiteral \| StringLiteral `                                              |                                                                                  |
| [58]                                                                             | `NumericLiteral`                                                                 | ::=                                                                              | ` IntegerLiteral \| DecimalLiteral \| DoubleLiteral `                            |                                                                                  |
| [59]                                                                             | `VarRef`                                                                         | ::=                                                                              | `"$" VarName `                                                                   |                                                                                  |
| [60]                                                                             | `VarName`                                                                        | ::=                                                                              | ` EQName `                                                                       |                                                                                  |
| [61]                                                                             | `ParenthesizedExpr`                                                              | ::=                                                                              | `"(" Expr? ")"`                                                                  |                                                                                  |
| [62]                                                                             | `ContextItemExpr`                                                                | ::=                                                                              | `"."`                                                                            |                                                                                  |
| [63]                                                                             | `FunctionCall`                                                                   | ::=                                                                              | ` EQName ArgumentList `                                                          | */* xgc: reserved-function-names */*                                             |
|                                                                                  |                                                                                  |                                                                                  |                                                                                  | */* gn: parens */*                                                               |
| [64]                                                                             | `Argument`                                                                       | ::=                                                                              | ` ExprSingle \| ArgumentPlaceholder `                                            |                                                                                  |
| [65]                                                                             | `ArgumentPlaceholder`                                                            | ::=                                                                              | `"?"`                                                                            |                                                                                  |
| [66]                                                                             | `FunctionItemExpr`                                                               | ::=                                                                              | ` NamedFunctionRef \| InlineFunctionExpr `                                       |                                                                                  |
| [67]                                                                             | `NamedFunctionRef`                                                               | ::=                                                                              | ` EQName "#" IntegerLiteral `                                                    | */* xgc: reserved-function-names */*                                             |
| [68]                                                                             | `InlineFunctionExpr`                                                             | ::=                                                                              | `"function" "(" ParamList? ")" ("as" SequenceType)? FunctionBody `               |                                                                                  |
| [69]                                                                             | `MapConstructor`                                                                 | ::=                                                                              | `"map" "{" (MapConstructorEntry ("," MapConstructorEntry)*)? "}"`                |                                                                                  |
| [70]                                                                             | `MapConstructorEntry`                                                            | ::=                                                                              | ` MapKeyExpr ":" MapValueExpr `                                                  |                                                                                  |
| [71]                                                                             | `MapKeyExpr`                                                                     | ::=                                                                              | ` ExprSingle `                                                                   |                                                                                  |
| [72]                                                                             | `MapValueExpr`                                                                   | ::=                                                                              | ` ExprSingle `                                                                   |                                                                                  |
| [73]                                                                             | `ArrayConstructor`                                                               | ::=                                                                              | ` SquareArrayConstructor \| CurlyArrayConstructor `                              |                                                                                  |
| [74]                                                                             | `SquareArrayConstructor`                                                         | ::=                                                                              | `"[" (ExprSingle ("," ExprSingle)*)? "]"`                                        |                                                                                  |
| [75]                                                                             | `CurlyArrayConstructor`                                                          | ::=                                                                              | `"array" EnclosedExpr `                                                          |                                                                                  |
| [76]                                                                             | `UnaryLookup`                                                                    | ::=                                                                              | `"?" KeySpecifier `                                                              |                                                                                  |
| [77]                                                                             | `SingleType`                                                                     | ::=                                                                              | ` SimpleTypeName "?"?`                                                           |                                                                                  |
| [78]                                                                             | `TypeDeclaration`                                                                | ::=                                                                              | `"as" SequenceType `                                                             |                                                                                  |
| [79]                                                                             | `SequenceType`                                                                   | ::=                                                                              | `("empty-sequence" "(" ")")\| (ItemType OccurrenceIndicator?)`                   |                                                                                  |
| [80]                                                                             | `OccurrenceIndicator`                                                            | ::=                                                                              | `"?" \| "*" \| "+"`                                                              | */* xgc: occurrence-indicators */*                                               |
| [81]                                                                             | `ItemType`                                                                       | ::=                                                                              | ` KindTest \| ("item" "(" ")") \| FunctionTest \| MapTest \| ArrayTest \| Atomic |                                                                                  |
| [82]                                                                             | `AtomicOrUnionType`                                                              | ::=                                                                              | ` EQName `                                                                       |                                                                                  |
| [83]                                                                             | `KindTest`                                                                       | ::=                                                                              | ` DocumentTest \| ElementTest \| AttributeTest \| SchemaElementTest \| SchemaAtt |                                                                                  |
| [84]                                                                             | `AnyKindTest`                                                                    | ::=                                                                              | `"node" "(" ")"`                                                                 |                                                                                  |
| [85]                                                                             | `DocumentTest`                                                                   | ::=                                                                              | `"document-node" "(" (ElementTest \| SchemaElementTest)? ")"`                    |                                                                                  |
| [86]                                                                             | `TextTest`                                                                       | ::=                                                                              | `"text" "(" ")"`                                                                 |                                                                                  |
| [87]                                                                             | `CommentTest`                                                                    | ::=                                                                              | `"comment" "(" ")"`                                                              |                                                                                  |
| [88]                                                                             | `NamespaceNodeTest`                                                              | ::=                                                                              | `"namespace-node" "(" ")"`                                                       |                                                                                  |
| [89]                                                                             | `PITest`                                                                         | ::=                                                                              | `"processing-instruction" "(" (NCName \| StringLiteral)? ")"`                    |                                                                                  |
| [90]                                                                             | `AttributeTest`                                                                  | ::=                                                                              | `"attribute" "(" (AttribNameOrWildcard ("," TypeName)?)? ")"`                    |                                                                                  |
| [91]                                                                             | `AttribNameOrWildcard`                                                           | ::=                                                                              | ` AttributeName \| "*"`                                                          |                                                                                  |
| [92]                                                                             | `SchemaAttributeTest`                                                            | ::=                                                                              | `"schema-attribute" "(" AttributeDeclaration ")"`                                |                                                                                  |
| [93]                                                                             | `AttributeDeclaration`                                                           | ::=                                                                              | ` AttributeName `                                                                |                                                                                  |
| [94]                                                                             | `ElementTest`                                                                    | ::=                                                                              | `"element" "(" (ElementNameOrWildcard ("," TypeName "?"?)?)? ")"`                |                                                                                  |
| [95]                                                                             | `ElementNameOrWildcard`                                                          | ::=                                                                              | ` ElementName \| "*"`                                                            |                                                                                  |
| [96]                                                                             | `SchemaElementTest`                                                              | ::=                                                                              | `"schema-element" "(" ElementDeclaration ")"`                                    |                                                                                  |
| [97]                                                                             | `ElementDeclaration`                                                             | ::=                                                                              | ` ElementName `                                                                  |                                                                                  |
| [98]                                                                             | `AttributeName`                                                                  | ::=                                                                              | ` EQName `                                                                       |                                                                                  |
| [99]                                                                             | `ElementName`                                                                    | ::=                                                                              | ` EQName `                                                                       |                                                                                  |
| [100]                                                                            | `SimpleTypeName`                                                                 | ::=                                                                              | ` TypeName `                                                                     |                                                                                  |
| [101]                                                                            | `TypeName`                                                                       | ::=                                                                              | ` EQName `                                                                       |                                                                                  |
| [102]                                                                            | `FunctionTest`                                                                   | ::=                                                                              | ` AnyFunctionTest \| TypedFunctionTest `                                         |                                                                                  |
| [103]                                                                            | `AnyFunctionTest`                                                                | ::=                                                                              | `"function" "(" "*" ")"`                                                         |                                                                                  |
| [104]                                                                            | `TypedFunctionTest`                                                              | ::=                                                                              | `"function" "(" (SequenceType ("," SequenceType)*)? ")" "as" SequenceType `      |                                                                                  |
| [105]                                                                            | `MapTest`                                                                        | ::=                                                                              | ` AnyMapTest \| TypedMapTest `                                                   |                                                                                  |
| [106]                                                                            | `AnyMapTest`                                                                     | ::=                                                                              | `"map" "(" "*" ")"`                                                              |                                                                                  |
| [107]                                                                            | `TypedMapTest`                                                                   | ::=                                                                              | `"map" "(" AtomicOrUnionType "," SequenceType ")"`                               |                                                                                  |
| [108]                                                                            | `ArrayTest`                                                                      | ::=                                                                              | ` AnyArrayTest \| TypedArrayTest `                                               |                                                                                  |
| [109]                                                                            | `AnyArrayTest`                                                                   | ::=                                                                              | `"array" "(" "*" ")"`                                                            |                                                                                  |
| [110]                                                                            | `TypedArrayTest`                                                                 | ::=                                                                              | `"array" "(" SequenceType ")"`                                                   |                                                                                  |
| [111]                                                                            | `ParenthesizedItemType`                                                          | ::=                                                                              | `"(" ItemType ")"`                                                               |                                                                                  |
| [112]                                                                            | `EQName`                                                                         | ::=                                                                              | ` QName \| URIQualifiedName `                                                    |                                                                                  |

#### A.1.1 Notation

[Definition: Each rule in the grammar defines one **symbol**, using the following format:

```
symbol ::= expression
```

]

[Definition: A **terminal** is a symbol or string or pattern that can appear in the right-hand side of a rule, but never appears on the left-hand side in the main grammar, although it may appear on the left-hand side of a rule in the grammar for terminals.] The following constructs are used to match strings of one or more characters in a terminal:
[a-zA-Z]

matches any Char with a value in the range(s) indicated (inclusive).
[abc]

matches any Char with a value among the characters enumerated.
[^abc]

matches any Char with a value not among the characters given.
"string"

matches the sequence of characters that appear inside the double quotes.
'string'

matches the sequence of characters that appear inside the single quotes.
[http://www.w3.org/TR/REC-example/#NT-Example]

matches any string matched by the production defined in the external specification as per the provided reference.

Patterns (including the above constructs) can be combined with grammatical operators to form more complex patterns, matching more complex sets of character strings. In the examples that follow, A and B represent (sub-)patterns.
(A)

`A` is treated as a unit and may be combined as described in this list.
A?

matches `A` or nothing; optional `A`.
A B

matches `A` followed by `B`. This operator has higher precedence than alternation; thus `A B | C D` is identical to `(A B) | (C D)`.
A | B

matches `A` or `B` but not both.
A - B

matches any string that matches `A` but does not match `B`.
A+

matches one or more occurrences of `A`. Concatenation has higher precedence than alternation; thus `A+ | B+` is identical to `(A+) | (B+)`.
A*

matches zero or more occurrences of `A`. Concatenation has higher precedence than alternation; thus `A* | B*` is identical to `(A*) | (B*)`

#### A.1.2 Extra-grammatical Constraints

This section contains constraints on the EBNF productions, which are required to parse syntactically valid sentences. The notes below are referenced from the right side of the production, with the notation: */* xgc: <id> */*.

**Constraint: leading-lone-slash**

A single slash may appear either as a complete path expression or as the first part of a path expression in which it is followed by a RelativePathExpr. In some cases, the next token after the slash is insufficient to allow a parser to distinguish these two possibilities: the `*` token and keywords like `union` could be either an operator or a NameTest . For example, without lookahead the first part of the expression `/ * 5` is easily taken to be a complete expression, `/ *`, which has a very different interpretation (the child nodes of `/`).

If the token immediately following a slash can form the start of a RelativePathExpr, then the slash must be the beginning of a PathExpr, not the entirety of it.

A single slash may be used as the left-hand argument of an operator by parenthesizing it: `(/) * 5`. The expression `5 * /`, on the other hand, is syntactically valid without parentheses.

**Constraint: xml-version**

The version of XML and XML Names (e.g. [XML 1.0] and [XML Names], or [XML 1.1] and [XML Names 1.1]) is implementation-defined. It is recommended that the latest applicable version be used (even if it is published later than this specification). The EBNF in this specification links only to the 1.0 versions. Note also that these external productions follow the whitespace rules of their respective specifications, and not the rules of this specification, in particular **A.2.4.1 Default Whitespace Handling**. Thus `prefix : localname` is not a syntactically valid lexical QName for purposes of this specification, just as it is not permitted in a XML document. Also, comments are not permissible on either side of the colon. Also extra-grammatical constraints such as well-formedness constraints must be taken into account.

**Constraint: reserved-function-names**

Unprefixed function names spelled the same way as language keywords could make the language impossible to parse. For instance, `element(foo)` could be taken either as a FunctionCall or as an ElementTest. Therefore, an unprefixed function name must not be any of the names in **A.3 Reserved Function Names**.

A function named "if" can be called by binding its namespace to a prefix and using the prefixed form: "library:if(foo)" instead of "if(foo)".

**Constraint: occurrence-indicators**

As written, the grammar in **A XPath 3.1 Grammar** is ambiguous for some forms using the '+' and '*' occurrence indicators. The ambiguity is resolved as follows: these operators are tightly bound to the SequenceType expression, and have higher precedence than other uses of these symbols. Any occurrence of '+' and '*', as well as '?', following a sequence type is assumed to be an occurrence indicator, which binds to the last ItemType in the SequenceType.

Thus, `4 treat as item() + - 5` must be interpreted as `(4 treat as item()+) - 5`, taking the '+' as an OccurrenceIndicator and the '-' as a subtraction operator. To force the interpretation of "+" as an addition operator (and the corresponding interpretation of the "-" as a unary minus), parentheses may be used: the form `(4 treat as item()) + -5` surrounds the SequenceType expression with parentheses and leads to the desired interpretation.

`function () as xs:string *` is interpreted as `function () as (xs:string *)`, not as `(function () as xs:string) *`. Parentheses can be used as shown to force the latter interpretation.

This rule has as a consequence that certain forms which would otherwise be syntactically valid and unambiguous are not recognized: in "4 treat as item() + 5", the "+" is taken as an OccurrenceIndicator, and not as an operator, which means this is not a syntactically valid expression.

#### A.1.3 Grammar Notes

This section contains general notes on the EBNF productions, which may be helpful in understanding how to interpret and implement the EBNF. These notes are not normative. The notes below are referenced from the right side of the production, with the notation: */* gn: <id> */*.

**Note:**

grammar-note: parens

Look-ahead is required to distinguish FunctionCall from a EQName or keyword followed by a Comment. For example: `address (: this may be empty :)` may be mistaken for a call to a function named "address" unless this lookahead is employed. Another example is `for (: whom the bell :) $tolls in 3 return $tolls`, where the keyword "for" must not be mistaken for a function name.

grammar-note: comments

Comments are allowed everywhere that ignorable whitespace is allowed, and the Comment symbol does not explicitly appear on the right-hand side of the grammar (except in its own production). See **A.2.4.1 Default Whitespace Handling**.

A comment can contain nested comments, as long as all "(:" and ":)" patterns are balanced, no matter where they occur within the outer comment.

**Note:**

Lexical analysis may typically handle nested comments by incrementing a counter for each "(:" pattern, and decrementing the counter for each ":)" pattern. The comment does not terminate until the counter is back to zero.

Some illustrative examples:

- `(: commenting out a (: comment :) may be confusing, but often helpful :)` is a syntactically valid Comment, since balanced nesting of comments is allowed.
- `"this is just a string :)"` is a syntactically valid expression. However, `(: "this is just a string :)" :)` will cause a syntax error. Likewise, `"this is another string (:"` is a syntactically valid expression, but `(: "this is another string (:" :)` will cause a syntax error. It is a limitation of nested comments that literal content can cause unbalanced nesting of comments.
- `for (: set up loop :) $i in $x return $i` is syntactically valid, ignoring the comment.
- `5 instance (: strange place for a comment :) of xs:integer` is also syntactically valid.

### A.2 Lexical structure

The terminal symbols assumed by the grammar above are described in this section.

Quoted strings appearing in production rules are terminal symbols.

Other terminal symbols are defined in **A.2.1 Terminal Symbols**.

Some productions are defined by reference to the XML and XML Names specifications (e.g. [XML 1.0] and [XML Names], or [XML 1.1] and [XML Names 1.1] . A host language may choose which version of these specifications is used; it is recommended that the latest applicable version be used (even if it is published later than this specification).

A **host language** may choose whether the lexical rules of [XML 1.0] and [XML Names] are followed, or alternatively, the lexical rules of [XML 1.1] and [XML Names 1.1] are followed.

When tokenizing, the longest possible match that is consistent with the EBNF is used.

All keywords are case sensitive. Keywords are not reserved—that is, any lexical QName may duplicate a keyword except as noted in **A.3 Reserved Function Names**.

#### A.2.1 Terminal Symbols

| [113]                                                                | `IntegerLiteral`                                                     | ::=                                                                  | ` Digits `                                                           |                                                                      |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [114]                                                                | `DecimalLiteral`                                                     | ::=                                                                  | `("." Digits) \| (Digits "." [0-9]*)`                                | */* ws: explicit */*                                                 |
| [115]                                                                | `DoubleLiteral`                                                      | ::=                                                                  | `(("." Digits) \| (Digits ("." [0-9]*)?)) [eE] [+-]? Digits `        | */* ws: explicit */*                                                 |
| [116]                                                                | `StringLiteral`                                                      | ::=                                                                  | `('"' (EscapeQuot \| [^"])* '"') \| ("'" (EscapeApos \| [^'])* "'")` | */* ws: explicit */*                                                 |
| [117]                                                                | `URIQualifiedName`                                                   | ::=                                                                  | ` BracedURILiteral NCName `                                          | */* ws: explicit */*                                                 |
| [118]                                                                | `BracedURILiteral`                                                   | ::=                                                                  | `"Q" "{" [^{}]* "}"`                                                 | */* ws: explicit */*                                                 |
| [119]                                                                | `EscapeQuot`                                                         | ::=                                                                  | `'""'`                                                               |                                                                      |
| [120]                                                                | `EscapeApos`                                                         | ::=                                                                  | `"''"`                                                               |                                                                      |
| [121]                                                                | `Comment`                                                            | ::=                                                                  | `"(:" (CommentContents \| Comment)* ":)"`                            | */* ws: explicit */*                                                 |
|                                                                      |                                                                      |                                                                      |                                                                      | */* gn: comments */*                                                 |
| [122]                                                                | `QName`                                                              | ::=                                                                  | ` [http://www.w3.org/TR/REC-xml-names/#NT-QName]Names `              | */* xgc: xml-version */*                                             |
| [123]                                                                | `NCName`                                                             | ::=                                                                  | ` [http://www.w3.org/TR/REC-xml-names/#NT-NCName]Names `             | */* xgc: xml-version */*                                             |
| [124]                                                                | `Char`                                                               | ::=                                                                  | ` [http://www.w3.org/TR/REC-xml#NT-Char]XML `                        | */* xgc: xml-version */*                                             |

The following symbols are used only in the definition of terminal symbols; they are not terminal symbols in the grammar of **A.1 EBNF**.

| [125]                                    | `Digits`                                 | ::=                                      | `[0-9]+`                                 |                                          |
| ---------------------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| [126]                                    | `CommentContents`                        | ::=                                      | `(Char+ - (Char* ('(:' \| ':)') Char*))` |                                          |

#### A.2.2 Terminal Delimitation

XPath 3.1 expressions consist of terminal symbols and symbol separators.

Terminal symbols that are not used exclusively in /* ws: explicit */ productions are of two kinds: delimiting and non-delimiting.

[Definition: The **delimiting terminal symbols** are: "!", "!=", StringLiteral, "#", "$", "(", ")", "*", "*:", "+", (comma), "-", (dot), "..", "/", "//", (colon), ":*", "::", ":=", "<", "<<", "<=", "=", "=>", ">", ">=", ">>", "?", "@", BracedURILiteral, "[", "]", "{", "|", "||", "}" ]

[Definition: The **non-delimiting terminal symbols** are: IntegerLiteral, URIQualifiedName, NCName, DecimalLiteral, DoubleLiteral, QName, "ancestor", "ancestor-or-self", "and", "array", "as", "attribute", "cast", "castable", "child", "comment", "descendant", "descendant-or-self", "div", "document-node", "element", "else", "empty-sequence", "eq", "every", "except", "following", "following-sibling", "for", "function", "ge", "gt", "idiv", "if", "in", "instance", "intersect", "is", "item", "le", "let", "lt", "map", "mod", "namespace", "namespace-node", "ne", "node", "of", "or", "parent", "preceding", "preceding-sibling", "processing-instruction", "return", "satisfies", "schema-attribute", "schema-element", "self", "some", "text", "then", "to", "treat", "union" ]

[Definition: Whitespace and Comments function as **symbol separators**. For the most part, they are not mentioned in the grammar, and may occur between any two terminal symbols mentioned in the grammar, except where that is forbidden by the /* ws: explicit */ annotation in the EBNF, or by the /* xgc: xml-version */ annotation.]

One or more symbol separators are required between two consecutive terminal symbols T and U (where T precedes U) when any of the following is true:

- T and U are both non-delimiting terminal symbols.
- T is a QName or an NCName and U is "." or "-".
- T is a numeric literal and U is ".", or vice versa.

#### A.2.3 End-of-Line Handling

The host language must specify whether the XPath 3.1 processor normalizes all line breaks on input, before parsing, and if it does so, whether it uses the rules of [XML 1.0] or [XML 1.1].

##### A.2.3.1 XML 1.0 End-of-Line Handling

For [XML 1.0] processing, all of the following must be translated to a single #xA character:

1. the two-character sequence #xD #xA
2. any #xD character that is not immediately followed by #xA.

##### A.2.3.2 XML 1.1 End-of-Line Handling

For [XML 1.1] processing, all of the following must be translated to a single #xA character:

1. the two-character sequence #xD #xA
2. the two-character sequence #xD #x85
3. the single character #x85
4. the single character #x2028
5. any #xD character that is not immediately followed by #xA or #x85.

#### A.2.4 Whitespace Rules

##### A.2.4.1 Default Whitespace Handling

[Definition: A **whitespace** character is any of the characters defined by [[http://www.w3.org/TR/REC-xml/#NT-S]](https://www.w3.org/TR/REC-xml/#NT-S).]

[Definition: **Ignorable whitespace** consists of any whitespace characters that may occur between terminals, unless these characters occur in the context of a production marked with a ws:explicit annotation, in which case they can occur only where explicitly specified (see **A.2.4.2 Explicit Whitespace Handling**).] Ignorable whitespace characters are not significant to the semantics of an expression. Whitespace is allowed before the first terminal and after the last terminal of an XPath expression. Whitespace is allowed between any two terminals. Comments may also act as "whitespace" to prevent two adjacent terminals from being recognized as one. Some illustrative examples are as follows:

- `foo- foo` results in a syntax error. "foo-" would be recognized as a QName.
- `foo -foo` is syntactically equivalent to `foo - foo`, two QNames separated by a subtraction operator.
- `foo(: This is a comment :)- foo` is syntactically equivalent to `foo - foo`. This is because the comment prevents the two adjacent terminals from being recognized as one.
- `foo-foo` is syntactically equivalent to single QName. This is because "-" is a valid character in a QName. When used as an operator after the characters of a name, the "-" must be separated from the name, e.g. by using whitespace or parentheses.
- `10div 3` results in a syntax error.
- `10 div3` also results in a syntax error.
- `10div3` also results in a syntax error.

##### A.2.4.2 Explicit Whitespace Handling

Explicit whitespace notation is specified with the EBNF productions, when it is different from the default rules, using the notation shown below. This notation is not inherited. In other words, if an EBNF rule is marked as /* ws: explicit */, the notation does not automatically apply to all the 'child' EBNF productions of that rule.

ws: explicit

/* ws: explicit */ means that the EBNF notation explicitly notates, with `S` or otherwise, where whitespace characters are allowed. In productions with the /* ws: explicit */ annotation, **A.2.4.1 Default Whitespace Handling** does not apply. Comments are not allowed in these productions except where the Comment non-terminal appears.

### A.3 Reserved Function Names

The following names are not allowed as function names in an unprefixed form because expression syntax takes precedence.

- `array`
- `attribute`
- `comment`
- `document-node`
- `element`
- `empty-sequence`
- `function`
- `if`
- `item`
- `map`
- `namespace-node`
- `node`
- `processing-instruction`
- `schema-attribute`
- `schema-element`
- `switch`
- `text`
- `typeswitch`

**Note:**

Although the keywords `switch` and `typeswitch` are not used in XPath, they are considered reserved function names for compatibility with XQuery.

### A.4 Precedence Order (Non-Normative)

The grammar in **A.1 EBNF** normatively defines built-in precedence among the operators of XPath. These operators are summarized here to make clear the order of their precedence from lowest to highest. The associativity column indicates the order in which operators of equal precedence in an expression are applied.
| #                                                       | Operator                                                | Associativity                                           |
| ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| 1                                                       | , (comma)                                               | either                                                  |
| 2                                                       | for, let, some, every, if                               | NA                                                      |
| 3                                                       | or                                                      | either                                                  |
| 4                                                       | and                                                     | either                                                  |
| 5                                                       | eq, ne, lt, le, gt, ge, =, !=, <, <=, >, >=, is, <<, >> | NA                                                      |
| 6                                                       | \|\|                                                    | left-to-right                                           |
| 7                                                       | to                                                      | NA                                                      |
| 8                                                       | +, - (binary)                                           | left-to-right                                           |
| 9                                                       | *, div, idiv, mod                                       | left-to-right                                           |
| 10                                                      | union, \|                                               | either                                                  |
| 11                                                      | intersect, except                                       | left-to-right                                           |
| 12                                                      | instance of                                             | NA                                                      |
| 13                                                      | treat as                                                | NA                                                      |
| 14                                                      | castable as                                             | NA                                                      |
| 15                                                      | cast as                                                 | NA                                                      |
| 16                                                      | =>                                                      | left-to-right                                           |
| 17                                                      | -, + (unary)                                            | right-to-left                                           |
| 18                                                      | !                                                       | left-to-right                                           |
| 19                                                      | /, //                                                   | left-to-right                                           |
| 20                                                      | [ ], ?                                                  | left-to-right                                           |
| 21                                                      | ? (unary)                                               | NA                                                      |

In the "Associativity" column, "either" indicates that all the operators at that level have the associative property (i.e., `(A op B) op C` is equivalent to `A op (B op C)`), so their associativity is inconsequential. "NA" (not applicable) indicates that the EBNF does not allow an expression that directly contains multiple operators from that precedence level, so the question of their associativity does not arise.

**Note:**

Parentheses can be used to override the operator precedence in the usual way. Square brackets in an expression such as A[B] serve two roles: they act as an operator causing B to be evaluated once for each item in the value of A, and they act as parentheses enclosing the expression B.

## B Type Promotion and Operator Mapping

### B.1 Type Promotion

[Definition: Under certain circumstances, an atomic value can be promoted from one type to another. **Type promotion** is used in evaluating function calls (see **3.1.5.1 Evaluating Static and Dynamic Function Calls**) and operators that accept numeric or string operands (see **B.2 Operator Mapping**).] The following type promotions are permitted:

1. Numeric type promotion: A value of type `xs:float` (or any type derived by restriction from `xs:float`) can be promoted to the type `xs:double`. The result is the `xs:double` value that is the same as the original value. A value of type `xs:decimal` (or any type derived by restriction from `xs:decimal`) can be promoted to either of the types `xs:float` or `xs:double`. The result of this promotion is created by casting the original value to the required type. This kind of promotion may cause loss of precision.
2. URI type promotion: A value of type `xs:anyURI` (or any type derived by restriction from `xs:anyURI`) can be promoted to the type `xs:string`. The result of this promotion is created by casting the original value to the type `xs:string`. **Note:** Since `xs:anyURI` values can be promoted to `xs:string`, functions and operators that compare strings using the default collation also compare `xs:anyURI` values using the default collation. This ensures that orderings that include strings, `xs:anyURI` values, or any combination of the two types are consistent and well-defined.

Note that type promotion is different from subtype substitution. For example:

- A function that expects a parameter `$p` of type `xs:float` can be invoked with a value of type `xs:decimal`. This is an example of type promotion. The value is actually converted to the expected type. Within the body of the function, `$p instance of xs:decimal` returns `false`.
- A function that expects a parameter `$p` of type `xs:decimal` can be invoked with a value of type `xs:integer`. This is an example of subtype substitution. The value retains its original type. Within the body of the function, `$p instance of xs:integer` returns `true`.

### B.2 Operator Mapping

The operator mapping tables in this section list the combinations of types for which the various operators of XPath 3.1 are defined. [Definition: For each operator and valid combination of operand types, the operator mapping tables specify a result type and an **operator function** that implements the semantics of the operator for the given types.] The definitions of the operator functions are given in [XQuery and XPath Functions and Operators 3.1]. The result of an operator may be the raising of an error by its operator function, as defined in [XQuery and XPath Functions and Operators 3.1]. The operator function fully defines the semantics of a given operator for the case where the operands are single atomic values of the types given in the table. For the definition of each operator (including its behavior for empty sequences or sequences of length greater than one), see the descriptive material in the main part of this document.

The `and` and `or` operators are defined directly in the main body of this document, and do not occur in the operator mapping tables.

If an operator in the operator mapping tables expects an operand of type *ET*, that operator can be applied to an operand of type *AT* if type *AT* can be converted to type *ET* by a combination of type promotion and subtype substitution. For example, a table entry indicates that the `gt` operator may be applied to two `xs:date` operands, returning `xs:boolean`. Therefore, the `gt` operator may also be applied to two (possibly different) subtypes of `xs:date`, also returning `xs:boolean`.

[Definition: When referring to a type, the term **numeric** denotes the types `xs:integer`, `xs:decimal`, `xs:float`, and `xs:double` which are all member types of the built-in union type `xs:numeric`.] An operator whose operands and result are designated as numeric might be thought of as representing four operators, one for each of the numeric types. For example, the numeric `+` operator might be thought of as representing the following four operators:
| Operator            | First operand type  | Second operand type | Result type         |
| ------------------- | ------------------- | ------------------- | ------------------- |
| `+`                 | `xs:integer`        | `xs:integer`        | `xs:integer`        |
| `+`                 | `xs:decimal`        | `xs:decimal`        | `xs:decimal`        |
| `+`                 | `xs:float`          | `xs:float`          | `xs:float`          |
| `+`                 | `xs:double`         | `xs:double`         | `xs:double`         |

A numeric operator may be validly applied to an operand of type *AT* if type *AT* can be converted to any of the four numeric types by a combination of type promotion and subtype substitution. If the result type of an operator is listed as numeric, it means "the first type in the ordered list `(xs:integer, xs:decimal, xs:float, xs:double)` into which all operands can be converted by subtype substitution and type promotion." As an example, suppose that the type `hatsize` is derived from `xs:integer` and the type `shoesize` is derived from `xs:float`. Then if the `+` operator is invoked with operands of type `hatsize` and `shoesize`, it returns a result of type `xs:float`. Similarly, if `+` is invoked with two operands of type `hatsize` it returns a result of type `xs:integer`.

[Definition: In the operator mapping tables, the term **Gregorian** refers to the types `xs:gYearMonth`, `xs:gYear`, `xs:gMonthDay`, `xs:gDay`, and `xs:gMonth`.] For binary operators that accept two Gregorian-type operands, both operands must have the same type (for example, if one operand is of type `xs:gDay`, the other operand must be of type `xs:gDay`.)
| Operator                                                | Type(A)                                                 | Type(B)                                                 | Function                                                | Result type                                             |
| ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| A + B                                                   | numeric                                                 | numeric                                                 | op:numeric-add(A, B)                                    | numeric                                                 |
| A + B                                                   | xs:date                                                 | xs:yearMonthDuration                                    | op:add-yearMonthDuration-to-date(A, B)                  | xs:date                                                 |
| A + B                                                   | xs:yearMonthDuration                                    | xs:date                                                 | op:add-yearMonthDuration-to-date(B, A)                  | xs:date                                                 |
| A + B                                                   | xs:date                                                 | xs:dayTimeDuration                                      | op:add-dayTimeDuration-to-date(A, B)                    | xs:date                                                 |
| A + B                                                   | xs:dayTimeDuration                                      | xs:date                                                 | op:add-dayTimeDuration-to-date(B, A)                    | xs:date                                                 |
| A + B                                                   | xs:time                                                 | xs:dayTimeDuration                                      | op:add-dayTimeDuration-to-time(A, B)                    | xs:time                                                 |
| A + B                                                   | xs:dayTimeDuration                                      | xs:time                                                 | op:add-dayTimeDuration-to-time(B, A)                    | xs:time                                                 |
| A + B                                                   | xs:dateTime                                             | xs:yearMonthDuration                                    | op:add-yearMonthDuration-to-dateTime(A, B)              | xs:dateTime                                             |
| A + B                                                   | xs:yearMonthDuration                                    | xs:dateTime                                             | op:add-yearMonthDuration-to-dateTime(B, A)              | xs:dateTime                                             |
| A + B                                                   | xs:dateTime                                             | xs:dayTimeDuration                                      | op:add-dayTimeDuration-to-dateTime(A, B)                | xs:dateTime                                             |
| A + B                                                   | xs:dayTimeDuration                                      | xs:dateTime                                             | op:add-dayTimeDuration-to-dateTime(B, A)                | xs:dateTime                                             |
| A + B                                                   | xs:yearMonthDuration                                    | xs:yearMonthDuration                                    | op:add-yearMonthDurations(A, B)                         | xs:yearMonthDuration                                    |
| A + B                                                   | xs:dayTimeDuration                                      | xs:dayTimeDuration                                      | op:add-dayTimeDurations(A, B)                           | xs:dayTimeDuration                                      |
| A - B                                                   | numeric                                                 | numeric                                                 | op:numeric-subtract(A, B)                               | numeric                                                 |
| A - B                                                   | xs:date                                                 | xs:date                                                 | op:subtract-dates(A, B)                                 | xs:dayTimeDuration                                      |
| A - B                                                   | xs:date                                                 | xs:yearMonthDuration                                    | op:subtract-yearMonthDuration-from-date(A, B)           | xs:date                                                 |
| A - B                                                   | xs:date                                                 | xs:dayTimeDuration                                      | op:subtract-dayTimeDuration-from-date(A, B)             | xs:date                                                 |
| A - B                                                   | xs:time                                                 | xs:time                                                 | op:subtract-times(A, B)                                 | xs:dayTimeDuration                                      |
| A - B                                                   | xs:time                                                 | xs:dayTimeDuration                                      | op:subtract-dayTimeDuration-from-time(A, B)             | xs:time                                                 |
| A - B                                                   | xs:dateTime                                             | xs:dateTime                                             | op:subtract-dateTimes(A, B)                             | xs:dayTimeDuration                                      |
| A - B                                                   | xs:dateTime                                             | xs:yearMonthDuration                                    | op:subtract-yearMonthDuration-from-dateTime(A, B)       | xs:dateTime                                             |
| A - B                                                   | xs:dateTime                                             | xs:dayTimeDuration                                      | op:subtract-dayTimeDuration-from-dateTime(A, B)         | xs:dateTime                                             |
| A - B                                                   | xs:yearMonthDuration                                    | xs:yearMonthDuration                                    | op:subtract-yearMonthDurations(A, B)                    | xs:yearMonthDuration                                    |
| A - B                                                   | xs:dayTimeDuration                                      | xs:dayTimeDuration                                      | op:subtract-dayTimeDurations(A, B)                      | xs:dayTimeDuration                                      |
| A * B                                                   | numeric                                                 | numeric                                                 | op:numeric-multiply(A, B)                               | numeric                                                 |
| A * B                                                   | xs:yearMonthDuration                                    | numeric                                                 | op:multiply-yearMonthDuration(A, B)                     | xs:yearMonthDuration                                    |
| A * B                                                   | numeric                                                 | xs:yearMonthDuration                                    | op:multiply-yearMonthDuration(B, A)                     | xs:yearMonthDuration                                    |
| A * B                                                   | xs:dayTimeDuration                                      | numeric                                                 | op:multiply-dayTimeDuration(A, B)                       | xs:dayTimeDuration                                      |
| A * B                                                   | numeric                                                 | xs:dayTimeDuration                                      | op:multiply-dayTimeDuration(B, A)                       | xs:dayTimeDuration                                      |
| A idiv B                                                | numeric                                                 | numeric                                                 | op:numeric-integer-divide(A, B)                         | xs:integer                                              |
| A div B                                                 | numeric                                                 | numeric                                                 | op:numeric-divide(A, B)                                 | numeric; but xs:decimal if both operands are xs:integer |
| A div B                                                 | xs:yearMonthDuration                                    | numeric                                                 | op:divide-yearMonthDuration(A, B)                       | xs:yearMonthDuration                                    |
| A div B                                                 | xs:dayTimeDuration                                      | numeric                                                 | op:divide-dayTimeDuration(A, B)                         | xs:dayTimeDuration                                      |
| A div B                                                 | xs:yearMonthDuration                                    | xs:yearMonthDuration                                    | op:divide-yearMonthDuration-by-yearMonthDuration (A, B) | xs:decimal                                              |
| A div B                                                 | xs:dayTimeDuration                                      | xs:dayTimeDuration                                      | op:divide-dayTimeDuration-by-dayTimeDuration (A, B)     | xs:decimal                                              |
| A mod B                                                 | numeric                                                 | numeric                                                 | op:numeric-mod(A, B)                                    | numeric                                                 |
| A eq B                                                  | numeric                                                 | numeric                                                 | op:numeric-equal(A, B)                                  | xs:boolean                                              |
| A eq B                                                  | xs:boolean                                              | xs:boolean                                              | op:boolean-equal(A, B)                                  | xs:boolean                                              |
| A eq B                                                  | xs:string                                               | xs:string                                               | op:numeric-equal(fn:compare(A, B), 0)                   | xs:boolean                                              |
| A eq B                                                  | xs:date                                                 | xs:date                                                 | op:date-equal(A, B)                                     | xs:boolean                                              |
| A eq B                                                  | xs:time                                                 | xs:time                                                 | op:time-equal(A, B)                                     | xs:boolean                                              |
| A eq B                                                  | xs:dateTime                                             | xs:dateTime                                             | op:dateTime-equal(A, B)                                 | xs:boolean                                              |
| A eq B                                                  | xs:duration                                             | xs:duration                                             | op:duration-equal(A, B)                                 | xs:boolean                                              |
| A eq B                                                  | Gregorian                                               | Gregorian                                               | op:gYear-equal(A, B) etc.                               | xs:boolean                                              |
| A eq B                                                  | xs:hexBinary                                            | xs:hexBinary                                            | op:hexBinary-equal(A, B)                                | xs:boolean                                              |
| A eq B                                                  | xs:base64Binary                                         | xs:base64Binary                                         | op:base64Binary-equal(A, B)                             | xs:boolean                                              |
| A eq B                                                  | xs:QName                                                | xs:QName                                                | op:QName-equal(A, B)                                    | xs:boolean                                              |
| A eq B                                                  | xs:NOTATION                                             | xs:NOTATION                                             | op:NOTATION-equal(A, B)                                 | xs:boolean                                              |
| A eq B                                                  | xs:hexBinary                                            | xs:hexBinary                                            | op:hexBinary-equal(A, B)                                | xs:boolean                                              |
| A eq B                                                  | xs:base64Binary                                         | xs:base64Binary                                         | op:hexBinary-equal(A, B)                                | xs:boolean                                              |
| A ne B                                                  | numeric                                                 | numeric                                                 | fn:not(op:numeric-equal(A, B))                          | xs:boolean                                              |
| A ne B                                                  | xs:boolean                                              | xs:boolean                                              | fn:not(op:boolean-equal(A, B))                          | xs:boolean                                              |
| A ne B                                                  | xs:string                                               | xs:string                                               | fn:not(op:numeric-equal(fn:compare(A, B), 0))           | xs:boolean                                              |
| A ne B                                                  | xs:date                                                 | xs:date                                                 | fn:not(op:date-equal(A, B))                             | xs:boolean                                              |
| A ne B                                                  | xs:time                                                 | xs:time                                                 | fn:not(op:time-equal(A, B))                             | xs:boolean                                              |
| A ne B                                                  | xs:dateTime                                             | xs:dateTime                                             | fn:not(op:dateTime-equal(A, B))                         | xs:boolean                                              |
| A ne B                                                  | xs:duration                                             | xs:duration                                             | fn:not(op:duration-equal(A, B))                         | xs:boolean                                              |
| A ne B                                                  | Gregorian                                               | Gregorian                                               | fn:not(op:gYear-equal(A, B)) etc.                       | xs:boolean                                              |
| A ne B                                                  | xs:hexBinary                                            | xs:hexBinary                                            | fn:not(op:hexBinary-equal(A, B))                        | xs:boolean                                              |
| A ne B                                                  | xs:base64Binary                                         | xs:base64Binary                                         | fn:not(op:base64Binary-equal(A, B))                     | xs:boolean                                              |
| A ne B                                                  | xs:QName                                                | xs:QName                                                | fn:not(op:QName-equal(A, B))                            | xs:boolean                                              |
| A ne B                                                  | xs:NOTATION                                             | xs:NOTATION                                             | fn:not(op:NOTATION-equal(A, B))                         | xs:boolean                                              |
| A ne B                                                  | xs:hexBinary                                            | xs:hexBinary                                            | fn:not(op:hexBinary-equal(A, B))                        | xs:boolean                                              |
| A ne B                                                  | xs:base64Binary                                         | xs:base64Binary                                         | fn:not(op:base64Binary-equal(A, B))                     | xs:boolean                                              |
| A gt B                                                  | numeric                                                 | numeric                                                 | op:numeric-greater-than(A, B)                           | xs:boolean                                              |
| A gt B                                                  | xs:boolean                                              | xs:boolean                                              | op:boolean-greater-than(A, B)                           | xs:boolean                                              |
| A gt B                                                  | xs:string                                               | xs:string                                               | op:numeric-greater-than(fn:compare(A, B), 0)            | xs:boolean                                              |
| A gt B                                                  | xs:date                                                 | xs:date                                                 | op:date-greater-than(A, B)                              | xs:boolean                                              |
| A gt B                                                  | xs:time                                                 | xs:time                                                 | op:time-greater-than(A, B)                              | xs:boolean                                              |
| A gt B                                                  | xs:dateTime                                             | xs:dateTime                                             | op:dateTime-greater-than(A, B)                          | xs:boolean                                              |
| A gt B                                                  | xs:yearMonthDuration                                    | xs:yearMonthDuration                                    | op:yearMonthDuration-greater-than(A, B)                 | xs:boolean                                              |
| A gt B                                                  | xs:dayTimeDuration                                      | xs:dayTimeDuration                                      | op:dayTimeDuration-greater-than(A, B)                   | xs:boolean                                              |
| A gt B                                                  | xs:hexBinary                                            | xs:hexBinary                                            | op:hexBinary-greater-than(A, B)                         | xs:boolean                                              |
| A gt B                                                  | xs:base64Binary                                         | xs:base64Binary                                         | op:base64Binary-greater-than(A, B)                      | xs:boolean                                              |
| A lt B                                                  | numeric                                                 | numeric                                                 | op:numeric-less-than(A, B)                              | xs:boolean                                              |
| A lt B                                                  | xs:boolean                                              | xs:boolean                                              | op:boolean-less-than(A, B)                              | xs:boolean                                              |
| A lt B                                                  | xs:string                                               | xs:string                                               | op:numeric-less-than(fn:compare(A, B), 0)               | xs:boolean                                              |
| A lt B                                                  | xs:date                                                 | xs:date                                                 | op:date-less-than(A, B)                                 | xs:boolean                                              |
| A lt B                                                  | xs:time                                                 | xs:time                                                 | op:time-less-than(A, B)                                 | xs:boolean                                              |
| A lt B                                                  | xs:dateTime                                             | xs:dateTime                                             | op:dateTime-less-than(A, B)                             | xs:boolean                                              |
| A lt B                                                  | xs:yearMonthDuration                                    | xs:yearMonthDuration                                    | op:yearMonthDuration-less-than(A, B)                    | xs:boolean                                              |
| A lt B                                                  | xs:dayTimeDuration                                      | xs:dayTimeDuration                                      | op:dayTimeDuration-less-than(A, B)                      | xs:boolean                                              |
| A lt B                                                  | xs:hexBinary                                            | xs:hexBinary                                            | op:hexBinary-less-than(A, B)                            | xs:boolean                                              |
| A lt B                                                  | xs:base64Binary                                         | xs:base64Binary                                         | op:base64Binary-less-than(A, B)                         | xs:boolean                                              |
| A ge B                                                  | numeric                                                 | numeric                                                 | op:numeric-greater-than(A, B) or op:numeric-equal(A, B) | xs:boolean                                              |
| A ge B                                                  | xs:boolean                                              | xs:boolean                                              | fn:not(op:boolean-less-than(A, B))                      | xs:boolean                                              |
| A ge B                                                  | xs:string                                               | xs:string                                               | op:numeric-greater-than(fn:compare(A, B), -1)           | xs:boolean                                              |
| A ge B                                                  | xs:date                                                 | xs:date                                                 | fn:not(op:date-less-than(A, B))                         | xs:boolean                                              |
| A ge B                                                  | xs:time                                                 | xs:time                                                 | fn:not(op:time-less-than(A, B))                         | xs:boolean                                              |
| A ge B                                                  | xs:dateTime                                             | xs:dateTime                                             | fn:not(op:dateTime-less-than(A, B))                     | xs:boolean                                              |
| A ge B                                                  | xs:yearMonthDuration                                    | xs:yearMonthDuration                                    | fn:not(op:yearMonthDuration-less-than(A, B))            | xs:boolean                                              |
| A ge B                                                  | xs:dayTimeDuration                                      | xs:dayTimeDuration                                      | fn:not(op:dayTimeDuration-less-than(A, B))              | xs:boolean                                              |
| A ge B                                                  | xs:hexBinary                                            | xs:hexBinary                                            | fn:not(op:hexBinary-less-than(A, B))                    | xs:boolean                                              |
| A ge B                                                  | xs:base64Binary                                         | xs:base64Binary                                         | fn:not(op:base64Binary-less-than(A, B))                 | xs:boolean                                              |
| A le B                                                  | numeric                                                 | numeric                                                 | op:numeric-less-than(A, B) or op:numeric-equal(A, B)    | xs:boolean                                              |
| A le B                                                  | xs:boolean                                              | xs:boolean                                              | fn:not(op:boolean-greater-than(A, B))                   | xs:boolean                                              |
| A le B                                                  | xs:string                                               | xs:string                                               | op:numeric-less-than(fn:compare(A, B), 1)               | xs:boolean                                              |
| A le B                                                  | xs:date                                                 | xs:date                                                 | fn:not(op:date-greater-than(A, B))                      | xs:boolean                                              |
| A le B                                                  | xs:time                                                 | xs:time                                                 | fn:not(op:time-greater-than(A, B))                      | xs:boolean                                              |
| A le B                                                  | xs:dateTime                                             | xs:dateTime                                             | fn:not(op:dateTime-greater-than(A, B))                  | xs:boolean                                              |
| A le B                                                  | xs:yearMonthDuration                                    | xs:yearMonthDuration                                    | fn:not(op:yearMonthDuration-greater-than(A, B))         | xs:boolean                                              |
| A le B                                                  | xs:dayTimeDuration                                      | xs:dayTimeDuration                                      | fn:not(op:dayTimeDuration-greater-than(A, B))           | xs:boolean                                              |
| A le B                                                  | xs:hexBinary                                            | xs:hexBinary                                            | fn:not(op:hexBinary-greater-than(A, B))                 | xs:boolean                                              |
| A le B                                                  | xs:base64Binary                                         | xs:base64Binary                                         | fn:not(op:base64Binary-greater-than(A, B))              | xs:boolean                                              |
| Operator                  | Operand type              | Function                  | Result type               |
| ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| + A                       | numeric                   | op:numeric-unary-plus(A)  | numeric                   |
| - A                       | numeric                   | op:numeric-unary-minus(A) | numeric                   |

## C Context Components

The tables in this section describe the scope (range of applicability) of the various components in a module's static context and dynamic context.

### C.1 Static Context Components

The following table describes the components of the **static context**. For each component, "global" indicates that the value of the component applies throughout an XPath expression, whereas "lexical" indicates that the value of the component applies only within the subexpression in which it is defined.
| Component                                                                        | Scope                                                                            |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| XPath 1.0 Compatibility Mode                                                     | global                                                                           |
| Statically known namespaces                                                      | global                                                                           |
| Default element/type namespace                                                   | global                                                                           |
| Default function namespace                                                       | global                                                                           |
| In-scope schema types                                                            | global                                                                           |
| In-scope element declarations                                                    | global                                                                           |
| In-scope attribute declarations                                                  | global                                                                           |
| In-scope variables                                                               | lexical; for-expressions, let-expressions, and quantified expressions can bind n |
| Context item static type                                                         | lexical                                                                          |
| Statically known function signatures                                             | global                                                                           |
| Statically known collations                                                      | global                                                                           |
| Default collation                                                                | global                                                                           |
| Base URI                                                                         | global                                                                           |
| Statically known documents                                                       | global                                                                           |
| Statically known collections                                                     | global                                                                           |
| Statically known default collection type                                         | global                                                                           |

### C.2 Dynamic Context Components

The following table describes how values are assigned to the various components of the **dynamic context**. All these components are initialized by mechanisms defined by the host language. For each component, "global" indicates that the value of the component remains constant throughout evaluation of the XPath expression, whereas "dynamic" indicates that the value of the component can be modified by the evaluation of subexpressions.
| Component                                                                        | Scope                                                                            |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Context item                                                                     | dynamic; changes during evaluation of path expressions and predicates            |
| Context position                                                                 | dynamic; changes during evaluation of path expressions and predicates            |
| Context size                                                                     | dynamic; changes during evaluation of path expressions and predicates            |
| Variable values                                                                  | dynamic; for-expressions, let-expressions, and quantified expressions can bind n |
| Current date and time                                                            | global; must be initialized                                                      |
| Implicit timezone                                                                | global; must be initialized                                                      |
| Available documents                                                              | global; must be initialized                                                      |
| Available collections                                                            | global; must be initialized                                                      |
| Default collection                                                               | global; overwriteable by implementation                                          |
| Available URI collections                                                        | global; must be initialized                                                      |
| Default URI collection                                                           | global; overwriteable by implementation                                          |

## D Implementation-Defined Items

The following items in this specification are implementation-defined:

1. The version of Unicode that is used to construct expressions.
2. The statically-known collations.
3. The implicit timezone.
4. The circumstances in which warnings are raised, and the ways in which warnings are handled.
5. The method by which errors are reported to the external processing environment.
6. Which version of XML and XML Names (e.g. [XML 1.0] and [XML Names] or [XML 1.1] and [XML Names 1.1]) and which version of XML Schema (e.g. [XML Schema 1.0] or [XML Schema 1.1]) is used for the definitions of primitives such as characters and names, and for the definitions of operations such as normalization of line endings and normalization of whitespace in attribute values. It is recommended that the latest applicable version be used (even if it is published later than this specification).
7. How XDM instances are created from sources other than an Infoset or PSVI.
8. Whether the implementation supports the namespace axis.
9. Whether the type system is based on [XML Schema 1.0] or [XML Schema 1.1]. An implementation that has based its type system on XML Schema 1.0 is not required to support the use of the `xs:dateTimeStamp` constructor or the use of `xs:dateTimeStamp` or `xs:error` as TypeName in any expression.
10. The signatures of functions provided by the implementation or via an implementation-defined API (see **2.1.1 Static Context**).
11. Any environment variables provided by the implementation.
12. Any rules used for static typing (see **2.2.3.1 Static Analysis Phase**).
13. Any serialization parameters provided by the implementation
14. What error, if any, is returned if an external function's implementation does not return the declared result type (see **2.2.4 Consistency Constraints**).

**Note:**

Additional implementation-defined items are listed in [XQuery and XPath Data Model (XDM) 3.1] and [XQuery and XPath Functions and Operators 3.1].

## E References

### E.1 Normative References

RFC2119
S. Bradner.
Key Words for use in RFCs to Indicate Requirement Levels.
IETF RFC 2119.
                        See
http://www.ietf.org/rfc/rfc2119.txt
.

RFC3986
T. Berners-Lee, R. Fielding, and
                        L. Masinter.
Uniform Resource Identifiers (URI): Generic
                           Syntax
. IETF RFC 3986.
                        See
http://www.ietf.org/rfc/rfc3986.txt
.

RFC3987
M. Duerst and M. Suignard.
Internationalized Resource Identifiers (IRIs)
.
                        IETF RFC 3987. See
http://www.ietf.org/rfc/rfc3987.txt
.

ISO/IEC 10646
ISO (International Organization for Standardization).
ISO/IEC 10646:2003. Information technology—Universal Multiple-Octet Coded Character
                           Set (UCS)
,
                        as, from time to time, amended, replaced by a new edition, or expanded by the addition
                        of new parts.
                        [Geneva]: International Organization for Standardization.
                        (See
http://www.iso.org
for the latest version.)

Unicode
The Unicode Consortium.
The Unicode Standard
Reading, Mass.: Addison-Wesley, 2003, as updated from time to time by the publication
                        of new versions.
                        See
http://www.unicode.org/standard/versions/
for the latest version and additional information on versions of the standard and
                        of the Unicode Character Database.
                        The version of Unicode to be used is
implementation-defined
,
                        but implementations are recommended to use the latest Unicode version.

XML 1.0
World Wide Web Consortium.
Extensible Markup Language (XML) 1.0.
W3C Recommendation.
                        See
http://www.w3.org/TR/REC-xml/
.
                        The edition of XML 1.0 must be no earlier than the Third Edition;
                        the edition used is
implementation-defined
,
                        but we recommend that implementations use the latest version.

XML 1.1
World Wide Web Consortium.
Extensible Markup Language (XML) 1.1.
W3C Recommendation.
                        See
http://www.w3.org/TR/xml11/

XML Base
World Wide Web Consortium.
XML Base.
W3C Recommendation. See
http://www.w3.org/TR/xmlbase/

XML Names
World Wide Web Consortium.
Namespaces in XML.
W3C Recommendation. See
http://www.w3.org/TR/REC-xml-names/

XML Names 1.1
World Wide Web Consortium.
Namespaces in XML 1.1.
W3C Recommendation. See
http://www.w3.org/TR/xml-names11/

XML ID
World Wide Web Consortium.
xml:id Version 1.0.
W3C Recommendation. See
http://www.w3.org/TR/xml-id/

XML Schema 1.0
World Wide Web Consortium.
XML Schema, Parts 0, 1, and 2 (Second Edition)
. W3C Recommendation, 28 October 2004.
                        See
http://www.w3.org/TR/xmlschema-0/
,
http://www.w3.org/TR/xmlschema-1/
,
                        and
http://www.w3.org/TR/xmlschema-2/
.

XML Schema 1.1
World Wide Web Consortium.
XML Schema, Parts 1, and 2
. W3C Recommendation 5 April 2012.
                        See
http://www.w3.org/TR/xmlschema11-1/
,
                        and
http://www.w3.org/TR/xmlschema11-2/
.

XQuery and XPath Data Model (XDM) 3.1
XQuery and XPath Data Model (XDM) 3.1
,
                        Norman Walsh, John Snelson, Andrew Coleman, Editors.
                        World Wide Web Consortium,
                        21 March 2017. 
                        This version is https://www.w3.org/TR/2017/REC-xpath-datamodel-31-20170321/.
                        The
latest version
is available at https://www.w3.org/TR/xpath-datamodel-31/.

XQuery and XPath Functions and Operators 3.1
XQuery and XPath Functions and Operators 3.1
,
                        Michael Kay, Editor.
                        World Wide Web Consortium,
                        21 March 2017. 
                        This version is https://www.w3.org/TR/2017/REC-xpath-functions-31-20170321/.
                        The
latest version
is available at https://www.w3.org/TR/xpath-functions-31/.

XSLT and XQuery Serialization 3.1
XSLT and XQuery Serialization 3.1
,
                        Andrew Coleman and Michael Sperberg-McQueen, Editors.
                        World Wide Web Consortium,
                        21 March 2017. 
                        This version is https://www.w3.org/TR/2017/REC-xslt-xquery-serialization-31-20170321/.
                        The
latest version
is available at https://www.w3.org/TR/xslt-xquery-serialization-31/.

### E.2 Non-normative References

XQuery 3.1: An XML Query Language
XQuery 3.1: An XML Query Language
,
                        Jonathan Robie, Michael Dyck and Josh Spiegel, Editors.
                        World Wide Web Consortium,
                        21 March 2017. 
                        This version is https://www.w3.org/TR/2017/REC-xquery-31-20170321/.
                        The
latest version
is available at https://www.w3.org/TR/xquery-31/.

XQuery 1.0 and XPath 2.0 Formal Semantics
XQuery 1.0 and XPath 2.0 Formal Semantics (Second Edition)
,
                        Jérôme Siméon, Denise Draper, Peter Frankhauser,
et. al.
, Editors.
                        World Wide Web Consortium,
                        14 December 2010.
                        This version is https://www.w3.org/TR/2010/REC-xquery-semantics-20101214/.
                        The
latest version
is available at https://www.w3.org/TR/xquery-semantics/.

XSL Transformations (XSLT) Version 3.0
XSL Transformations (XSLT) Version 3.0
,
                        Michael Kay, Editor.
                        World Wide Web Consortium,
                        7 February 2017. 
                        This version is https://www.w3.org/TR/2017/CR-xslt-30-20170207/.
                        The
latest version
is available at https://www.w3.org/TR/xslt-30/.

XML Infoset
World Wide Web
                        Consortium.
XML Information Set
(Second Edition).
W3C Recommendation
4 February 2004.
See
http://www.w3.org/TR/xml-infoset/

XML Path Language (XPath) Version 1.0
XML Path Language (XPath) Version 1.0
, James Clark and Steven DeRose, Editors. World Wide Web Consortium, 16 Nov 1999.
                        This version is http://www.w3.org/TR/1999/REC-xpath-19991116. The
latest version
is available at http://www.w3.org/TR/xpath.

XML Path Language (XPath) Version 2.0
XML Path Language (XPath) 2.0 (Second Edition)
,
                        Don Chamberlin, Anders Berglund, Scott Boag,
et. al.
, Editors.
                        World Wide Web Consortium,
                        14 December 2010.
                        This version is https://www.w3.org/TR/2010/REC-xpath20-20101214/.
                        The
latest version
is available at https://www.w3.org/TR/xpath20/.

XML Path Language (XPath) Version 3.0
XML Path Language (XPath) 3.0
,
                        Jonathan Robie, Don Chamberlin, Michael Dyck, John Snelson, Editors.
                        World Wide Web Consortium,
                        08 April 2014. 
                        This version is https://www.w3.org/TR/2014/REC-xpath-30-20140408/.
                        The
latest version
is available at https://www.w3.org/TR/xpath-30/.

XPointer
World Wide Web Consortium.
XML
                           Pointer Language (XPointer).
W3C Last Call Working Draft 8 January 2001.
                        See
http://www.w3.org/TR/WD-xptr

### E.3 Background Material

Character Model
World Wide Web Consortium.
Character Model for the World Wide Web.
W3C Working
                        Draft. See
http://www.w3.org/TR/charmod/
.

XSL Transformations (XSLT) Version 1.0
XSL Transformations (XSLT) Version 1.0
, James Clark, Editor. World Wide Web Consortium, 16 Nov 1999. This version is http://www.w3.org/TR/1999/REC-xslt-19991116.
                        The
latest version
is available at http://www.w3.org/TR/xslt.

## F Error Conditions

err:XPST0001

It is a static error if analysis of an expression relies on some component of the static context that is [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31.

err:XPDY0002

It is a dynamic error if evaluation of an expression relies on some part of the dynamic context that is [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31.

err:XPST0003

It is a static error if an expression is not a valid instance of the grammar defined in **A.1 EBNF**.

err:XPTY0004

It is a type error if, during the static analysis phase, an expression is found to have a static type that is not appropriate for the context in which the expression occurs, or during the dynamic evaluation phase, the dynamic type of a value does not match a required type as specified by the matching rules in **2.5.5 SequenceType Matching**.

err:XPST0005

During the analysis phase, it is a static error if the static type assigned to an expression other than the expression `()` or `data(())` is `empty-sequence()`.

err:XPST0008

It is a static error if an expression refers to an element name, attribute name, schema type name, namespace prefix, or variable name that is not defined in the static context, except for an ElementName in an ElementTest or an AttributeName in an AttributeTest.

err:XPST0010

An implementation that does not support the namespace axis must raise a static error if it encounters a reference to the namespace axis and XPath 1.0 compatibility mode is false.

err:XPST0017

It is a static error if the expanded QName and number of arguments in a static function call do not match the name and arity of a function signature in the static context.

err:XPTY0018

It is a type error if the result of a path operator contains both nodes and non-nodes.

err:XPTY0019

It is a type error if `E1` in a path expression `E1/E2` does not evaluate to a sequence of nodes.

err:XPTY0020

It is a type error if, in an axis step, the context item is not a node.

err:XQST0039

It is a static error for an inline function expression to have more than one parameter with the same name.

err:XQST0046

An implementation MAY raise a static error if the value of a BracedURILiteral is of nonzero length and is neither an absolute URI nor a relative URI.

err:XPDY0050

It is a dynamic error if the dynamic type of the operand of a `treat` expression does not match the sequence type specified by the `treat` expression. This error might also be raised by a path expression beginning with "`/`" or "`//`" if the context node is not in a tree that is rooted at a document node. This is because a leading "`/`" or "`//`" in a path expression is an abbreviation for an initial step that includes the clause `treat as document-node()`.

err:XPST0051

It is a static error if the expanded QName for an AtomicOrUnionType in a SequenceType is not defined in the in-scope schema types as a generalized atomic type.

err:XQST0052

The type named in a cast or castable expression must be the name of a type defined in the in-scope schema types, and the type must be `simple`.

err:XQST0070

A static error is raised if any of the following conditions is statically detected in any expression:

- The prefix `xml` is bound to some namespace URI other than `http://www.w3.org/XML/1998/namespace`.
- A prefix other than `xml` is bound to the namespace URI `http://www.w3.org/XML/1998/namespace`.
- The prefix `xmlns` is bound to any namespace URI.
- A prefix other than `xmlns` is bound to the namespace URI `http://www.w3.org/2000/xmlns/`.

err:XPST0080

It is a static error if the target type of a `cast` or `castable` expression is `xs:NOTATION`, `xs:anySimpleType`, or `xs:anyAtomicType`.

err:XPST0081

It is a static error if a QName used in an expression contains a namespace prefix that cannot be expanded into a namespace URI by using the statically known namespaces.

err:XPTY0117

When applying the function conversion rules, if an item is of type `xs:untypedAtomic` and the expected type is namespace-sensitive, a type error [err:XPTY0117] is raised.

err:XPDY0130

An implementation-dependent limit has been exceeded.

err:XQST0134

The namespace axis is not supported.

err:XQDY0137

No two keys in a map may have the same key value.

## G Glossary (Non-Normative)

Gregorian

In the operator mapping tables, the term **Gregorian** refers to the types `xs:gYearMonth`, `xs:gYear`, `xs:gMonthDay`, `xs:gDay`, and `xs:gMonth`.

NaN

**NaN** is the string used to represent the double value NaN (not-a-number); the default value is the string "NaN"

SequenceType matching

**SequenceType matching** compares the dynamic type of a value with an expected sequence type.

Static Base URI

**Static Base URI.** This is an absolute URI, used to resolve relative URI references.

URI

Within this specification, the term **URI** refers to a Universal Resource Identifier as defined in [RFC3986] and extended in [RFC3987] with the new name **IRI**.

XDM instance

The term **XDM instance** is used, synonymously with the term value, to denote an unconstrained sequence of items.

XPath 1.0 compatibility     mode

**XPath 1.0 compatibility mode.** This value is `true` if rules for backward compatibility with XPath Version 1.0 are in effect; otherwise it is `false`.

anonymous function

An **anonymous function** is a function with no name. Anonymous functions may be created, for example, by evaluating an inline function expression or by partial function application.

argument expression

An argument to a function call is either an **argument expression** or an ArgumentPlaceholder ("?").

argument value

Argument expressions are evaluated with respect to DC, producing **argument values**.

arity

The number of `Argument`s in an `ArgumentList` is its **arity**.

array

An **array** is a function that associates a set of positions, represented as positive integer keys, with values.

arrow operator

An **arrow operator** applies a function to the value of an expression, using the value as the first argument to the function.

associated value

The value associated with a given key is called the **associated value** of the key.

atomic value

An **atomic value** is a value in the value space of an **atomic type**, as defined in [XML Schema 1.0] or [XML Schema 1.1].

atomization

**Atomization** of a sequence is defined as the result of invoking the `fn:data` function, as defined in [Section 2.4 fn:data](https://www.w3.org/TR/xpath-functions-31/#func-data)FO31.

available documents

**Available documents.** This is a mapping of strings to document nodes. Each string represents the absolute URI of a resource. The document node is the root of a tree that represents that resource using the data model. The document node is returned by the `fn:doc` function when applied to that URI.

available item collections

**Available collections.** This is a mapping of strings to sequences of items. Each string represents the absolute URI of a resource. The sequence of items represents the result of the `fn:collection` function when that URI is supplied as the argument.

available text resources

**Available text resources**. This is a mapping of strings to text resources. Each string represents the absolute URI of a resource. The resource is returned by the `fn:unparsed-text` function when applied to that URI.

available uri collections

**Available URI collections.** This is a mapping of strings to sequences of URIs. The string represents the absolute URI of a resource which can be interpreted as an aggregation of a number of individual resources each of which has its own URI. The sequence of URIs represents the result of the `fn:uri-collection` function when that URI is supplied as the argument.

axis step

An **axis step** returns a sequence of nodes that are reachable from the context node via a specified axis. Such a step has two parts: an **axis**, which defines the "direction of movement" for the step, and a node test, which selects nodes based on their kind, name, and/or type annotation.

built-in function

The **built-in functions** are the functions defined in [XQuery and XPath Functions and Operators 3.1] in the `http://www.w3.org/2005/xpath-functions`, `http://www.w3.org/2001/XMLSchema`, `http://www.w3.org/2005/xpath-functions/math`, `http://www.w3.org/2005/xpath-functions/map`, and `http://www.w3.org/2005/xpath-functions/array` namespaces.

collation

A **collation** is a specification of the manner in which strings and URIs are compared and, by extension, ordered. For a more complete definition of collation, see [Section 5.3 Comparison of strings](https://www.w3.org/TR/xpath-functions-31/#string-compare)FO31.

comma operator

One way to construct a sequence is by using the **comma operator**, which evaluates each of its operands and concatenates the resulting sequences, in order, into a single result sequence.

constructor function

The **constructor function** for a given type is used to convert instances of other simple types into the given type. The semantics of the constructor function call `T($arg)` are defined to be equivalent to the expression `(($arg) cast as T?)`.

content expression

In an enclosed expression, the optional expression enclosed in curly braces is called the **content expression**.

context item

The **context item** is the item currently being processed.

context item static type

**Context item static type.** This component defines the static type of the context item within the scope of a given expression.

context node

When the context item is a node, it can also be referred to as the **context node**.

context position

The **context position** is the position of the context item within the sequence of items currently being processed.

context size

The **context size** is the number of items in the sequence of items currently being processed.

current dateTime

**Current dateTime.** This information represents an implementation-dependent point in time during the processing of an expression, and includes an explicit timezone. It can be retrieved by the `fn:current-dateTime` function. If invoked multiple times during the execution of an expression, this function always returns the same result.

data model

XPath 3.1 operates on the abstract, logical structure of an XML document or JSON object, rather than its surface syntax. This logical structure, known as the **data model**, is defined in [XQuery and XPath Data Model (XDM) 3.1].

decimal-separator

**decimal-separator** is the character used to separate the integer part of the number from the fractional part, both in the picture string and in the formatted number; the default value is the period character (.)

default URI collection

**Default URI collection.** This is the sequence of URIs that would result from calling the `fn:uri-collection` function with no arguments.

default calendar

**Default calendar.** This is the calendar used when formatting dates in human-readable output (for example, by the functions `fn:format-date` and `fn:format-dateTime`) if no other calendar is requested. The value is a string.

default collation

**Default collation.** This identifies one of the collations in statically known collations as the collation to be used by functions and operators for comparing and ordering values of type `xs:string` and `xs:anyURI` (and types derived from them) when no explicit collation is specified.

default collection

**Default collection.** This is the sequence of items that would result from calling the `fn:collection` function with no arguments.

default element/type namespace

**Default element/type namespace.** This is a namespace URI or [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31. The namespace URI, if present, is used for any unprefixed QName appearing in a position where an element or type name is expected.

default function namespace

**Default function namespace.** This is a namespace URI or [absent](https://www.w3.org/TR/xpath-datamodel-31/#dt-absent)DM31. The namespace URI, if present, is used for any unprefixed QName appearing in a position where a function name is expected.

default language

**Default language.** This is the natural language used when creating human-readable output (for example, by the functions `fn:format-date` and `fn:format-integer`) if no other language is requested. The value is a language code as defined by the type `xs:language`.

default place

**Default place.** This is a geographical location used to identify the place where events happened (or will happen) when formatting dates and times using functions such as `fn:format-date` and `fn:format-dateTime`, if no other place is specified. It is used when translating timezone offsets to civil timezone names, and when using calendars where the translation from ISO dates/times to a local representation is dependent on geographical location. Possible representations of this information are an ISO country code or an Olson timezone name, but implementations are free to use other representations from which the above information can be derived.

delimiting terminal symbol

The **delimiting terminal symbols** are: "!", "!=", StringLiteral, "#", "$", "(", ")", "*", "*:", "+", (comma), "-", (dot), "..", "/", "//", (colon), ":*", "::", ":=", "<", "<<", "<=", "=", "=>", ">", ">=", ">>", "?", "@", BracedURILiteral, "[", "]", "{", "|", "||", "}"

digit

**digit** is a character used in the picture string to represent an optional digit; the default value is the number sign character (#)

document order

Informally, **document order** is the order in which nodes appear in the XML serialization of a document.

dynamic context

The **dynamic context** of an expression is defined as information that is needed for the dynamic evaluation of an expression.

dynamic error

A **dynamic error** is an error that must be detected during the dynamic evaluation phase and may be detected during the static analysis phase. Numeric overflow is an example of a dynamic error.

dynamic evaluation phase

The **dynamic evaluation phase** is the phase during which the value of an expression is computed.

dynamic function call

A **dynamic function call** consists of a base expression that returns the function and a parenthesized list of zero or more arguments (argument expressions or ArgumentPlaceholders).

dynamic type

A **dynamic type** is associated with each value as it is computed. The dynamic type of a value may be more specific than the static type of the expression that computed it (for example, the static type of an expression might be `xs:integer*`, denoting a sequence of zero or more integers, but at evaluation time its value may have the dynamic type `xs:integer`, denoting exactly one integer.)

effective boolean value

The **effective boolean value** of a value is defined as the result of applying the `fn:boolean` function to the value, as defined in [Section 7.3.1 fn:boolean](https://www.w3.org/TR/xpath-functions-31/#func-boolean)FO31.

empty sequence

A sequence containing zero items is called an **empty sequence**.

enclosed expression

An **enclosed expression** is an instance of the EnclosedExpr production, which allows an optional expression within curly braces.

entry

Each key / value pair in a map is called an **entry**.

environment variables

**Environment variables.** This is a mapping from names to values. Both the names and the values are strings. The names are compared using an implementation-defined collation, and are unique under this collation. The set of environment variables is implementation-defined and **may** be empty.

error value

In addition to its identifying QName, a dynamic error may also carry a descriptive string and one or more additional values called **error values**.

expanded QName

An **expanded QName** is a triple: its components are a prefix, a local name, and a namespace URI. In the case of a name in no namespace, the namespace URI and prefix are both absent. In the case of a name in the default namespace, the prefix is absent.

exponent-separator

**exponent-separator** is the character used to separate the mantissa from the exponent in scientific notation both in the picture string and in the formatted number; the default value is the character (e).

expression context

The **expression context** for a given expression consists of all the information that can affect the result of the expression.

external function

**External functions** are functions that are implemented outside the query environment.

filter expression

An expression followed by a predicate (that is, `E1[E2]`) is referred to as a **filter expression**: its effect is to return those items from the value of `E1` that satisfy the predicate in E2.

fixed position

In a partial function application, a **fixed position** is an argument/parameter position for which the `ArgumentList` has an argument expression (as opposed to an `ArgumentPlaceholder`).

focus

The first three components of the dynamic context (context item, context position, and context size) are called the **focus** of the expression.

function coercion

**Function coercion** wraps a [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31 in a new function with signature the same as the expected type. This effectively delays the checking of the argument and return types until the function is invoked.

function conversion rules

The **function conversion rules** are used to convert an argument value to its expected type; that is, to the declared type of the function parameter.

generalized atomic type

A **generalized atomic type** is a type which is either (a) an atomic type or (b) a pure union type

grouping-separator

**grouping-separator** is the character typically used as a thousands separator, both in the picture string and in the formatted number; the default value is the comma character (,)

host language function

A **host language function** is an external function defined by the host language.

host-language

A **host language** for XPath is a language or specification that incorporates XPath as a sublanguage and that defines how the static and dynamic context for evaluation of XPath expressions are to be established.

ignorable whitespace

**Ignorable whitespace** consists of any whitespace characters that may occur between terminals, unless these characters occur in the context of a production marked with a ws:explicit annotation, in which case they can occur only where explicitly specified (see **A.2.4.2 Explicit Whitespace Handling**).

implementation   dependent

**Implementation-dependent** indicates an aspect that may differ between implementations, is not specified by this or any W3C specification, and is not required to be specified by the implementor for any particular implementation.

implementation defined

**Implementation-defined** indicates an aspect that may differ between implementations, but must be specified by the implementor for each particular implementation.

implementation-defined function

An **implementation-defined function** is an external function that is implementation-defined

implicit timezone

**Implicit timezone.** This is the timezone to be used when a date, time, or dateTime value that does not have a timezone is used in a comparison or arithmetic operation. The implicit timezone is an implementation-defined value of type `xs:dayTimeDuration`. See [Section 3.2.7.3 Timezones](https://www.w3.org/TR/xmlschema-2/#dateTime-timezones)XS1-2 or [Section 3.3.7 dateTime](https://www.w3.org/TR/xmlschema11-2/#dateTime)XS11-2 for the range of valid values of a timezone.

in-scope attribute declarations

**In-scope attribute declarations.** Each attribute declaration is identified either by an expanded QName (for a top-level attribute declaration) or by an implementation-dependent attribute identifier (for a local attribute declaration).

in-scope element declarations

**In-scope element declarations.** Each element declaration is identified either by an expanded QName (for a top-level element declaration) or by an implementation-dependent element identifier (for a local element declaration).

in-scope namespaces

The **in-scope namespaces** property of an element node is a set of namespace bindings, each of which associates a namespace prefix with a URI.

in-scope schema definitions

**In-scope schema definitions.** This is a generic term for all the element declarations, attribute declarations, and schema type definitions that are in scope during static analysis of an expression.

in-scope schema type

**In-scope schema types.** Each schema type definition is identified either by an expanded QName (for a **named type**) or by an implementation-dependent type identifier (for an **anonymous type**). The in-scope schema types include the predefined schema types described in **2.5.1 Predefined Schema Types**.

in-scope variables

**In-scope variables.** This is a mapping from expanded QName to type. It defines the set of variables that are available for reference within an expression. The expanded QName is the name of the variable, and the type is the static type of the variable.

infinity

**infinity** is the string used to represent the double value infinity (`INF`); the default value is the string "Infinity"

inline function expression

An **inline function expression** creates an anonymous function defined directly in the inline function expression.

item

An **item** is either an atomic value, a node, or a [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31.

kind test

An alternative form of a node test called a **kind test** can select nodes based on their kind, name, and type annotation.

lexical QName

A **lexical QName** is a name that conforms to the syntax of the QName production

literal

A **literal** is a direct syntactic representation of an atomic value.

map

A **map** is a function that associates a set of keys with values, resulting in a collection of key / value pairs.

may

**MAY** means that an item is truly optional.

member

The values of an array are called its **members**.

minus-sign

**minus-sign** is the single character used to mark negative numbers; the default value is the hyphen-minus character (#x2D).

must

**MUST** means that the item is an absolute requirement of the specification.

must not

**MUST NOT** means that the item is an absolute prohibition of the specification.

name test

A node test that consists only of an EQName or a Wildcard is called a **name test**.

named function

A **named function** is a function defined in the static context for the expression. To uniquely identify a particular named function, both its name as an expanded QName and its arity are required.

named function reference

A **named function reference** is an expression which evaluates to a named function. The name and arity of the returned function are known statically, and correspond to a function signature present in the static context; if the function is context dependent, then the returned function is associated with the static context of the named function reference and the dynamic context in which it is evaluated.

named functions

**Named functions**. This is a mapping from (expanded QName, arity) to [function](https://www.w3.org/TR/xpath-datamodel-31/#dt-function-item)DM31.

namespace-sensitive

The **namespace-sensitive** types are `xs:QName`, `xs:NOTATION`, types derived by restriction from `xs:QName` or `xs:NOTATION`, list types that have a namespace-sensitive item type, and union types with a namespace-sensitive type in their transitive membership.

node

A **node** is an instance of one of the **node kinds** defined in [Section 6 Nodes](https://www.w3.org/TR/xpath-datamodel-31/#Node)DM31.

node test

A **node test** is a condition on the name, kind (element, attribute, text, document, comment, or processing instruction), and/or type annotation of a node. A node test determines which nodes contained by an axis are selected by a step.

non-delimiting terminal symbol

The **non-delimiting terminal symbols** are: IntegerLiteral, URIQualifiedName, NCName, DecimalLiteral, DoubleLiteral, QName, "ancestor", "ancestor-or-self", "and", "array", "as", "attribute", "cast", "castable", "child", "comment", "descendant", "descendant-or-self", "div", "document-node", "element", "else", "empty-sequence", "eq", "every", "except", "following", "following-sibling", "for", "function", "ge", "gt", "idiv", "if", "in", "instance", "intersect", "is", "item", "le", "let", "lt", "map", "mod", "namespace", "namespace-node", "ne", "node", "of", "or", "parent", "preceding", "preceding-sibling", "processing-instruction", "return", "satisfies", "schema-attribute", "schema-element", "self", "some", "text", "then", "to", "treat", "union"

numeric

When referring to a type, the term **numeric** denotes the types `xs:integer`, `xs:decimal`, `xs:float`, and `xs:double` which are all member types of the built-in union type `xs:numeric`.

operator function

For each operator and valid combination of operand types, the operator mapping tables specify a result type and an **operator function** that implements the semantics of the operator for the given types.

partial function application

A static or dynamic function call is a **partial function application** if one or more arguments is an ArgumentPlaceholder.

partially applied function

A **partially applied function** is a function created by partial function application.

path expression

A **path expression** can be used to locate nodes within trees. A path expression consists of a series of one or more steps, separated by "`/`" or "`//`", and optionally beginning with "`/`" or "`//`".

pattern-separator

**pattern-separator** is a character used to separate positive and negative sub-pictures in a picture string; the default value is the semi-colon character (;)

per-mille

**per-mille** is the character used both in the picture string and in the formatted number to indicate that the number is written as a per-thousand fraction; the default value is the Unicode per-mille character (#x2030)

percent

**percent** is the character used both in the picture string and in the formatted number to indicate that the number is written as a per-hundred fraction; the default value is the percent character (%)

primary expression

**Primary expressions** are the basic primitives of the language. They include literals, variable references, context item expressions, and function calls. A primary expression may also be created by enclosing any expression in parentheses, which is sometimes helpful in controlling the precedence of operators.

principal node kind

Every axis has a **principal node kind**. If an axis can contain elements, then the principal node kind is element; otherwise, it is the kind of nodes that the axis can contain.

pure union type

A **pure union type** is an XML Schema union type that satisfies the following constraints: (1) `{variety}` is `union`, (2) the `{facets}` property is empty, (3) no type in the transitive membership of the union type has `{variety}` `list`, and (4) no type in the transitive membership of the union type is a type with `{variety}` `union` having a non-empty `{facets}` property

resolve

To **resolve a relative URI** `$rel` against a base URI `$base` is to expand it to an absolute URI, as if by calling the function `fn:resolve-uri($rel, $base)`.

reverse document order

The node ordering that is the reverse of document order is called **reverse document order**.

same key

Two atomic values `K1` and `K2` have the **same key value** if `op:same-key(K1, K2)` returns `true`, as specified in [Section 17.1.1 op:same-key](https://www.w3.org/TR/xpath-functions-31/#func-same-key)FO31

schema type

A **schema type** is a type that is (or could be) defined using the facilities of [XML Schema 1.0] or [XML Schema 1.1] (including the built-in types).

sequence

A **sequence** is an ordered collection of zero or more items.

sequence type

A **sequence type** is a type that can be expressed using the SequenceType syntax. Sequence types are used whenever it is necessary to refer to a type in an XPath 3.1 expression. The term **sequence type** suggests that this syntax is used to describe the type of an XPath 3.1 value, which is always a sequence.

singleton

A sequence containing exactly one item is called a **singleton**.

singleton focus

A **singleton focus** is a focus that refers to a single item; in a singleton focus, context item is set to the item, context position = 1 and context size = 1.

stable

Document order is **stable**, which means that the relative order of two nodes will not change during the processing of a given expression, even if this order is implementation-dependent.

static analysis phase

The **static analysis phase** depends on the expression itself and on the static context. The **static analysis phase** does not depend on input data (other than schemas).

static context

The **static context** of an expression is the information that is available during static analysis of the expression, prior to its evaluation.

static error

An error that can be detected during the static analysis phase, and is not a type error, is a **static error**.

static function call

A **static function call** consists of an EQName followed by a parenthesized list of zero or more arguments.

static type

The **static type** of an expression is the best inference that the processor is able to make statically about the type of the result of the expression.

static typing feature

The **Static Typing Feature** is an optional feature of XPath that provides support for static semantics, and requires implementations to detect and report type errors during the static analysis phase.

statically known  collections

**Statically known collections.** This is a mapping from strings to types. The string represents the absolute URI of a resource that is potentially available using the `fn:collection` function. The type is the type of the sequence of items that would result from calling the `fn:collection` function with this URI as its argument.

statically known  documents

**Statically known documents.** This is a mapping from strings to types. The string represents the absolute URI of a resource that is potentially available using the `fn:doc` function. The type is the static type of a call to `fn:doc` with the given URI as its literal argument.

statically known collations

**Statically known collations.** This is an implementation-defined mapping from URI to collation. It defines the names of the collations that are available for use in processing expressions.

statically known decimal formats

**Statically known decimal formats.** This is a mapping from QNames to decimal formats, with one default format that has no visible name, referred to as the unnamed decimal format. Each format is available for use when formatting numbers using the `fn:format-number` function.

statically known default collection type

**Statically known default collection type.** This is the type of the sequence of items that would result from calling the `fn:collection` function with no arguments.

statically known function signatures

**Statically known function signatures.** This is a mapping from (expanded QName, arity) to [function signature](https://www.w3.org/TR/xpath-datamodel-31/#dt-signature)DM31.

statically known namespaces

**Statically known namespaces.** This is a mapping from prefix to namespace URI that defines all the namespaces that are known during static processing of a given expression.

step

A **step** is a part of a path expression that generates a sequence of items and then filters the sequence by zero or more predicates. The value of the step consists of those items that satisfy the predicates, working from left to right. A step may be either an axis step or a postfix expression.

string value

The **string value** of a node is a string and can be extracted by applying the [Section 2.3 fn:string](https://www.w3.org/TR/xpath-functions-31/#func-string)FO31 function to the node.

substitution group

**Substitution groups** are defined in [Section 2.2.2.2 Element Substitution Group](https://www.w3.org/TR/xmlschema-1/#Element_Equivalence_Class)XS1-1 and [Section 2.2.2.2 Element Substitution Group](https://www.w3.org/TR/xmlschema11-1/#Element_Equivalence_Class)XS11-1. Informally, the substitution group headed by a given element (called the **head element**) consists of the set of elements that can be substituted for the head element without affecting the outcome of schema validation.

subtype

A sequence type `A` is a **subtype** of a sequence type `B` if the judgement `subtype(A, B)` is true.

subtype substitution

The use of a value whose dynamic type is derived from an expected type is known as **subtype substitution**.

symbol

Each rule in the grammar defines one **symbol**, using the following format:

```
symbol ::= expression
```

symbol separators

Whitespace and Comments function as **symbol separators**. For the most part, they are not mentioned in the grammar, and may occur between any two terminal symbols mentioned in the grammar, except where that is forbidden by the /* ws: explicit */ annotation in the EBNF, or by the /* xgc: xml-version */ annotation.

terminal

A **terminal** is a symbol or string or pattern that can appear in the right-hand side of a rule, but never appears on the left-hand side in the main grammar, although it may appear on the left-hand side of a rule in the grammar for terminals.

type annotation

Each element node and attribute node in an XDM instance has a **type annotation** (described in [Section 2.7 Schema Information](https://www.w3.org/TR/xpath-datamodel-31/#types)DM31). The type annotation of a node is a reference to an XML Schema type.

type error

A **type error** may be raised during the static analysis phase or the dynamic evaluation phase. During the static analysis phase, a type error occurs when the static type of an expression does not match the expected type of the context in which the expression occurs. During the dynamic evaluation phase, a type error occurs when the dynamic type of a value does not match the expected type of the context in which the value occurs.

type promotion

Under certain circumstances, an atomic value can be promoted from one type to another. **Type promotion** is used in evaluating function calls (see **3.1.5.1 Evaluating Static and Dynamic Function Calls**) and operators that accept numeric or string operands (see **B.2 Operator Mapping**).

typed value

The **typed value** of a node is a sequence of atomic values and can be extracted by applying the [Section 2.4 fn:data](https://www.w3.org/TR/xpath-functions-31/#func-data)FO31 function to the node.

value

In the data model, a **value** is always a sequence.

variable reference

A **variable reference** is an EQName preceded by a $-sign.

variable values

**Variable values**. This is a mapping from expanded QName to value. It contains the same expanded QNames as the in-scope variables in the static context for the expression. The expanded QName is the name of the variable and the value is the dynamic value of the variable, which includes its dynamic type.

warning

In addition to static errors, dynamic errors, and type errors, an XPath 3.1 implementation may raise **warnings**, either during the static analysis phase or the dynamic evaluation phase. The circumstances in which warnings are raised, and the ways in which warnings are handled, are implementation-defined.

whitespace

A **whitespace** character is any of the characters defined by [[http://www.w3.org/TR/REC-xml/#NT-S]](https://www.w3.org/TR/REC-xml/#NT-S).

xs:anyAtomicType

`xs:anyAtomicType` is an atomic type that includes all atomic values (and no values that are not atomic). Its base type is `xs:anySimpleType` from which all simple types, including atomic, list, and union types, are derived. All primitive atomic types, such as `xs:decimal` and `xs:string`, have `xs:anyAtomicType` as their base type.

xs:dayTimeDuration

`xs:dayTimeDuration` is derived by restriction from `xs:duration`. The lexical representation of `xs:dayTimeDuration` is restricted to contain only day, hour, minute, and second components.

xs:error

`xs:error` is a simple type with no value space. It is defined in [Section 3.16.7.3 xs:error](https://www.w3.org/TR/xmlschema11-1/#xsd-error)XS11-1 and can be used in the **2.5.4 SequenceType Syntax** to raise errors.

xs:untyped

`xs:untyped` is used as the type annotation of an element node that has not been validated, or has been validated in `skip` mode.

xs:untypedAtomic

`xs:untypedAtomic` is an atomic type that is used to denote untyped atomic data, such as text that has not been assigned a more specific type.

xs:yearMonthDuration

`xs:yearMonthDuration` is derived by restriction from `xs:duration`. The lexical representation of `xs:yearMonthDuration` is restricted to contain only year and month components.

zero-digit

**zero-digit** is the character used to represent the digit zero; the default value is the Western digit zero (#x30). This character must be a digit (category Nd in the Unicode property database), and it must have the numeric value zero. This property implicitly defines the ten Unicode characters that are used to represent the values 0 to 9: Unicode is organized so that each set of decimal digits forms a contiguous block of characters in numerical sequence. Within the picture string any of these ten character can be used (interchangeably) as a place-holder for a mandatory digit. Within the final result string, these ten characters are used to represent the digits zero to nine.

## H Backwards Compatibility (Non-Normative)

### H.1 Incompatibilities relative to XPath 3.0

The following names are now reserved, and cannot appear as function names (see **A.3 Reserved Function Names**):

- `map`
- `array`

### H.2 Incompatibilities relative to XPath 2.0

The following names are now reserved, and cannot appear as function names (see **A.3 Reserved Function Names**):

- `function`
- `namespace-node`
- `switch`

If `U` is a union type with `T` as one of its members, and if `E` is an element with `T` as its type annotation, the expression `E instance of element(*, U)` returns `true` in both XPath 3.0 and 3.1. In XPath 2.0, it returns `false`.

**Note:**

This is not an incompatibility with XPath 3.0. It should be included in XPath 3.0 as an incompatibility with XPath 2.0 but it was discovered after publication.

### H.3 Incompatibilities relative to XPath 1.0

This appendix provides a summary of the areas of incompatibility between XPath 3.1 and [XML Path Language (XPath) Version 1.0]. In each of these cases, an XPath 3.1 processor is compatible with an XPath 2.0 processor or an XPath 3.0 processor.

Three separate cases are considered:

1. Incompatibilities that exist when source documents have no schema, and when running with XPath 1.0 compatibility mode set to true. This specification has been designed to reduce the number of incompatibilities in this situation to an absolute minimum, but some differences remain and are listed individually.
2. Incompatibilities that arise when XPath 1.0 compatibility mode is set to false. In this case, the number of expressions where compatibility is lost is rather greater.
3. Incompatibilities that arise when the source document is processed using a schema (whether or not XPath 1.0 compatibility mode is set to true). Processing the document with a schema changes the way that the values of nodes are interpreted, and this can cause an XPath expression to return different results.

#### H.3.1 Incompatibilities when Compatibility Mode is true

The list below contains all known areas, within the scope of this specification, where an XPath 3.1 processor running with compatibility mode set to true will produce different results from an XPath 1.0 processor evaluating the same expression, assuming that the expression was valid in XPath 1.0, and that the nodes in the source document have no type annotations other than `xs:untyped` and `xs:untypedAtomic`.

Incompatibilities in the behavior of individual functions are not listed here, but are included in an appendix of [XQuery and XPath Functions and Operators 3.1].

Since both XPath 1.0 and XPath 3.1 leave some aspects of the specification implementation-defined, there may be incompatibilities in the behavior of a particular implementation that are outside the scope of this specification. Equally, some aspects of the behavior of XPath are defined by the host language.

1. Consecutive comparison operators such as `A < B < C` were supported in XPath 1.0, but are not permitted by the XPath 3.1 grammar. In most cases such comparisons in XPath 1.0 did not have the intuitive meaning, so it is unlikely that they have been widely used in practice. If such a construct is found, an XPath 3.1 processor will report a syntax error, and the construct can be rewritten as `(A < B) < C`
2. When converting strings to numbers (either explicitly when using the `number` function, or implicitly say on a function call), certain strings that converted to the special value `NaN` under XPath 1.0 will convert to values other than `NaN` under XPath 3.1. These include any number written with a leading `+` sign, any number in exponential floating point notation (for example `1.0e+9`), and the strings `INF` and `-INF`. Furthermore, the strings `Infinity` and `-Infinity`, which were accepted by XPath 1.0 as representations of the floating-point values positive and negative infinity, are no longer recognized. They are converted to `NaN` when running under XPath 3.1 with compatibility mode set to true, and cause a dynamic error when compatibility mode is set to false.
3. XPath 3.1 does not allow a token starting with a letter to follow immediately after a numeric literal, without intervening whitespace. For example, `10div 3` was permitted in XPath 1.0, but in XPath 3.1 must be written as `10 div 3`.
4. The namespace axis is deprecated as of XPath 2.0. Implementations may support the namespace axis for backward compatibility with XPath 1.0, but they are not required to do so. (XSLT 2.0 requires that if XPath backwards compatibility mode is supported, then the namespace axis must also be supported; but other host languages may define the conformance rules differently.)
5. In XPath 1.0, the expression `-x|y` parsed as `-(x|y)`, and returned the negation of the numeric value of the first node in the union of `x` and `y`. In XPath 3.1, this expression parses as `(-x)|y`. When XPath 1.0 Compatibility Mode is true, this will always cause a type error.
6. The rules for converting numbers to strings have changed. These may affect the way numbers are displayed in the output of a stylesheet. For numbers whose absolute value is in the range `1E-6` to `1E+6`, the result should be the same, but outside this range, scientific format is used for non-integral `xs:float` and `xs:double` values.
7. If one operand in a general comparison is a single atomic value of type `xs:boolean`, the other operand is converted to `xs:boolean` when XPath 1.0 compatibility mode is set to true. In XPath 1.0, if neither operand of a comparison operation using the <, <=, > or >= operator was a node set, both operands were converted to numbers. The result of the expression `true() > number('0.5')` is therefore true in XPath 1.0, but is false in XPath 3.1 even when compatibility mode is set to true.
8. In XPath 3.1, a type error is raised if the PITarget specified in a SequenceType of form `processing-instruction(PITarget)` is not a valid NCName. In XPath 1.0, this condition was not treated as an error.

#### H.3.2 Incompatibilities when Compatibility Mode is false

Even when the setting of the XPath 1.0 compatibility mode is false, many XPath expressions will still produce the same results under XPath 3.1 as under XPath 1.0. The exceptions are described in this section.

In all cases it is assumed that the expression in question was valid under XPath 1.0, that XPath 1.0 compatibility mode is false, and that all elements and attributes are annotated with the types `xs:untyped` and `xs:untypedAtomic` respectively.

In the description below, the terms *node-set* and *number* are used with their XPath 1.0 meanings, that is, to describe expressions which according to the rules of XPath 1.0 would have generated a node-set or a number respectively.

1. When a node-set containing more than one node is supplied as an argument to a function or operator that expects a single node or value, the XPath 1.0 rule was that all nodes after the first were discarded. Under XPath 3.1, a type error occurs if there is more than one node. The XPath 1.0 behavior can always be restored by using the predicate `[1]` to explicitly select the first node in the node-set.
2. In XPath 1.0, the `<` and `>` operators, when applied to two strings, attempted to convert both the strings to numbers and then made a numeric comparison between the results. In XPath 3.1, these operators perform a string comparison using the default collating sequence. (If either value is numeric, however, the results are compatible with XPath 1.0)
3. When an empty node-set is supplied as an argument to a function or operator that expects a number, the value is no longer converted implicitly to NaN. The XPath 1.0 behavior can always be restored by using the `number` function to perform an explicit conversion.
4. More generally, the supplied arguments to a function or operator are no longer implicitly converted to the required type, except in the case where the supplied argument is of type `xs:untypedAtomic` (which will commonly be the case when a node in a schemaless document is supplied as the argument). For example, the function call `substring-before(10 div 3, ".")` raises a type error under XPath 3.1, because the arguments to the `substring-before` function must be strings rather than numbers. The XPath 1.0 behavior can be restored by performing an explicit conversion to the required type using a constructor function or cast.
5. The rules for comparing a node-set to a boolean have changed. In XPath 1.0, an expression such as `$node-set = true()` was evaluated by converting the node-set to a boolean and then performing a boolean comparison: so this expression would return `true` if `$node-set` was non-empty. In XPath 3.1, this expression is handled in the same way as other comparisons between a sequence and a singleton: it is `true` if `$node-set` contains at least one node whose value, after atomization and conversion to a boolean using the casting rules, is `true`. This means that if `$node-set` is empty, the result under XPath 3.1 will be `false` regardless of the value of the boolean operand, and regardless of which operator is used. If `$node-set` is non-empty, then in most cases the comparison with a boolean is likely to fail, giving a dynamic error. But if a node has the value "0", "1", "true", or "false", evaluation of the expression may succeed.
6. Comparisons of a number to a boolean, a number to a string, or a string to a boolean are not allowed in XPath 3.1: they result in a type error. In XPath 1.0 such comparisons were allowed, and were handled by converting one of the operands to the type of the other. So for example in XPath 1.0 `4 = true()` was true; `4 = "+4"` was false (because the string `+4` converts to `NaN`), and `false = "false"` was false (because the string `"false"` converts to the boolean `true`). In XPath 3.0 all these comparisons are type errors.
7. Additional numeric types have been introduced, with the effect that arithmetic may now be done as an integer, decimal, or single- or double-precision floating point calculation where previously it was always performed as double-precision floating point. The result of the `div` operator when dividing two integers is now a value of type decimal rather than double. The expression `10 div 0` raises an error rather than returning positive infinity.
8. The rules for converting strings to numbers have changed. The implicit conversion that occurs when passing an `xs:untypedAtomic` value as an argument to a function that expects a number no longer converts unrecognized strings to the value `NaN`; instead, it reports a dynamic error. This is in addition to the differences that apply when backwards compatibility mode is set to true.
9. Many operations in XPath 3.1 produce an empty sequence as their result when one of the arguments or operands is an empty sequence. Where the operation expects a string, an empty sequence is usually considered equivalent to a zero-length string, which is compatible with the XPath 1.0 behavior. Where the operation expects a number, however, the result is not the same. For example, if `@width` returns an empty sequence, then in XPath 1.0 the result of `@width+1` was `NaN`, while with XPath 3.1 it is `()`. This has the effect that a filter expression such as `item[@width+1 != 2]` will select items having no `width` attribute under XPath 1.0, and will not select them under XPath 3.1.
10. The typed value of a comment node, processing instruction node, or namespace node under XPath 3.1 is of type `xs:string`, not `xs:untypedAtomic`. This means that no implicit conversions are applied if the value is used in a context where a number is expected. If a processing-instruction node is used as an operand of an arithmetic operator, for example, XPath 1.0 would attempt to convert the string value of the node to a number (and deliver `NaN` if unsuccessful), while XPath 3.1 will report a type error.
11. In XPath 1.0, it was defined that with an expression of the form `A and B`, B would not be evaluated if A was false. Similarly in the case of `A or B`, B would not be evaluated if A was true. This is no longer guaranteed with XPath 3.1: the implementation is free to evaluate the two operands in either order or in parallel. This change has been made to give more scope for optimization in situations where XPath expressions are evaluated against large data collections supported by indexes. Implementations may choose to retain backwards compatibility in this area, but they are not obliged to do so.
12. In XPath 1.0, the expression `-x|y` parsed as `-(x|y)`, and returned the negation of the numeric value of the first node in the union of `x` and `y`. In XPath 3.1, this expression parses as `(-x)|y`. When XPath 1.0 Compatibility Mode is false, this will cause a type error, except in the situation where `x` evaluates to an empty sequence. In that situation, XPath 3.1 will return the value of `y`, whereas XPath 1.0 returned the negation of the numeric value of `y`.

#### H.3.3 Incompatibilities when using a Schema

An XPath expression applied to a document that has been processed against a schema will not always give the same results as the same expression applied to the same document in the absence of a schema. Since schema processing had no effect on the result of an XPath 1.0 expression, this may give rise to further incompatibilities. This section gives a few examples of the differences that can arise.

Suppose that the context node is an element node derived from the following markup: `<background color="red green blue"/>`. In XPath 1.0, the predicate `[@color="blue"]` would return `false`. In XPath 3.1, if the `color` attribute is defined in a schema to be of type `xs:NMTOKENS`, the same predicate will return `true`.

Similarly, consider the expression `@birth < @death` applied to the element `<person birth="1901-06-06" death="1991-05-09"/>`. With XPath 1.0, this expression would return false, because both attributes are converted to numbers, which returns `NaN` in each case. With XPath 3.1, in the presence of a schema that annotates these attributes as dates, the expression returns `true`.

Once schema validation is applied, elements and attributes cannot be used as operands and arguments of expressions that expect a different data type. For example, it is no longer possible to apply the `substring` function to a date to extract the year component, or to a number to extract the integer part. Similarly, if an attribute is annotated as a boolean then it is not possible to compare it with the strings `"true"` or `"false"`. All such operations lead to type errors. The remedy when such errors occur is to introduce an explicit conversion, or to do the computation in a different way. For example, `substring-after(@temperature, "-")` might be rewritten as `abs(@temperature)`.

In the case of an XPath 3.1 implementation that provides the static typing feature, many further type errors will be reported in respect of expressions that worked under XPath 1.0. For example, an expression such as `round(../@price)` might lead to a static type error because the processor cannot infer statically that `../@price` is guaranteed to be numeric.

Schema validation will in many cases perform whitespace normalization on the contents of elements (depending on their type). This will change the result of operations such as the `string-length` function.

Schema validation augments the data model by adding default values for omitted attributes and empty elements.

## I Change Log (Non-Normative)

This appendix lists the changes that have been made to this specification since the publication of XPath 3.0 Recommendation.

### I.1 Changes since the Candidate Recommendation of 17 December 2015

#### I.1.1 Substantive Changes

1. Added switch expressions to list of conditional expressions in **2.3.4 Errors and Optimization**. Resolves [Bug 29320](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29320).
2. If the content expression is not provided explicitly, the content expression is `()`. Previously, no content expression was provided, but the value of the content was specified. This caused problems evaluating functions with empty bodies, and failed to provide a host language expression for the function implementation in the data model.
3. Partial function application never returns a map or an array. If `$F` is a map or an array, then `$F(?)` is a partial function application that returns a function, but the function it returns is not a map nor an array. Resolves action A-640-03.
4. Added `xs:anySimpleType` to the list of types that have no contructor function. Resolves [Bug 29583](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29583).
5. Added requirement to specify minimum values for some date and time functions. Resolves [Bug 29576](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29576).
6. Changed the rules for atomization in lookup in **3.11.3 The Lookup Operator ("?") for Maps and Arrays**. Resolves [Bug 29622](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29622).
7. Allowed more specific typing of maps, arrays, and functions. Affects **2.5.5.8 Map Test**, **2.5.5.9 Array Test**, **2.5.6.2 The judgement subtype-itemtype(Ai, Bi)**, **3.1.5.1 Evaluating Static and Dynamic Function Calls**, and **3.1.7 Inline Function Expressions**. Resolves [Bug 29586](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29586).
8. Changed **3.11.1.2 Map Lookup using Function Call Syntax** to define semantics using only [Section 17.1.6 map:get](https://www.w3.org/TR/xpath-functions-31/#func-map-get)FO31, changed **3.11.2.2 Array Lookup using Function Call Syntax** to define semantics using only [Section 17.3.2 array:get](https://www.w3.org/TR/xpath-functions-31/#func-array-get)FO31, thus aligning edge cases and eliminating the possibility of discrepancies creeping in. Resolves [Bug 29683](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29683).

#### I.1.2 Editorial Changes

1. Significantly changed the prose in **3.1.5.1 Evaluating Static and Dynamic Function Calls**. Resolves [Bug 29277](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29277).
2. Created formal definitions for implementation-defined function and host language function.
3. Fixed a problem with conditional text in **2.5.6.2 The judgement subtype-itemtype(Ai, Bi)**: `Bi` is ` function(*)`, `Ai` is a FunctionTest. Resolves [Bug 29414](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29414).
4. Changed definition of same key, redefining it in terms of [Section 17.1.1 op:same-key](https://www.w3.org/TR/xpath-functions-31/#func-same-key)FO31. Resolves [Bug 29362](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29362).
5. Moved definition of enclosed expression to prevent it from disappearing in XPath. Resolves [Bug 29382](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29382).
6. Modified **4 Conformance** to be more consistent with RFC2119. Resolves [Bug 29498](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29498).
7. Deleted erroneous note in **3.11.3.1 Unary Lookup** that claimed `array?*` is equivalent to `array:flatten`. Resolves [Bug 29487](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29487).
8. Provided definitions of implementation-defined function, moved definition of external function , added definition of host language function. Eliminated references to "host programming languages". Clarified wording on external function declarations. Resolves [Bug 29509](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29509).
9. Removed a dangling otherwise clause that belonged to the XQuery specification. Resolves [Bug 29693](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29693).
10. Made EBNF productions in the document body look the same as those in Appendix A (by adding production annotations to the former), thus eliminating the need to specify which is normative.
11. Clarified ambiguous wording about comments in **A.2.4.2 Explicit Whitespace Handling**. Resolves [Bug 29700](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29700).

### I.2 Changes introduced in the Candidate Recommendation of 17 December 2015

#### I.2.1 Substantive Changes

1. Significant rewrite of **2.5.7 xs:error**. Resolves [Bug 29119](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29119).
2. Removed non-normative description of casting rules, referring to the normative definition instead. Resolves [Bug 29192](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29192).
3. To allow streaming, context size may be undefined in an XPath implementation, in which case `last()` raises an error. Resolves [Bug 29227](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29227).
4. Clarified semantics of external context item declaration in library modules. Resolves [Bug 29246](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29246).
5. In **2.1.1 Static Context**, clarified that only function signatures that are present in the static context — not actual function implementations. Resolves [Bug 28175](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28175).
6. Changed rules for same key value to improve handling of maps in which keys may or may not have timezones. Resolves [Bug 28632](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28632) and [Bug 28729](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28729).
7. The precedence of the **3.16 Arrow operator (=>)** has changed. Resolves [Bug 27537](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27537).
8. The error when atomizing a function, map, or array is `[err:FOTY0013]`, not `[err:FOTY0012]`. Resolves [Bug 27610](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27610).
9. Collections can now contain any item. This affects statically known collections, statically known collection type, available collections (formerly known as available node collections, default collection (formerly known as default node collection, **2.2.4 Consistency Constraints**, **2.4.4 Input Sources**.
10. Fixed outdated text that restricted constructor functions to atomic or generalized atomic types. Resolves [Bug 28915](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28915).
11. Changed the semantics of **3.11.3.2 Postfix Lookup** . Resolves [Bug 27536](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27536), fixing inadequacies in the earlier resolution.

#### I.2.2 Editorial Changes

1. Refactored the grammar to use `EnclosedExpr` consistently.
2. Added a paragraph clarifying the type of an array as a function. Resolves [Bug 29260](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29260).
3. Clarified how function coercion applies to maps and arrays using two examples. Resolves [Bug 27059](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27059).
4. Removed nine operators from **B.2 Operator Mapping** to eliminate redundant specification. Resolves [Bug 22456](https://www.w3.org/Bugs/Public/show_bug.cgi?id=22456).
5. Modified **4 Conformance** to use the term MUST NOT. Resolves [Bug 28023](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28023).
6. Added explicit semantics for NCName in **3.11.3 The Lookup Operator ("?") for Maps and Arrays**. Resolves [Bug 28701](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28701).
7. Deleted obsolete discussion of named function references and `xs:numeric`. Resolves [Bug 28081](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28081).
8. Removed the unused definition of the initial context item. Resolves [Bug 28905](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28905).
9. Significantly changed description of names in **2 Basics**. Resolves [Bug 28241](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28241).
10. Fixed a number of dangling references to XQuery/XPath 3.0 where 3.1 was intended. Resolves [Bug 28782](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28782).
11. Clarified the text in **H Backwards Compatibility** about SequenceType matching and union types. Resolves [Bug 28894](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28894).
12. Renamed Available Resource Collections to Available URI Collections, renamed Available Node Collections to Available Collections, renamed Default Resource Collection to Default URI Collection, renamed Default Node Collection to Default Collection. Resolves [Bug 28957](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28957).
13. Clarified the definition of built-in functions. Resolves [Bug 28282](https://www.w3.org/Bugs/Public/show_bug.cgi?id=28282).
14. Clarified the text in **3.16 Arrow operator (=>)**. Resolves [Bug 29346](https://www.w3.org/Bugs/Public/show_bug.cgi?id=29346).

### I.3 Changes introduced in the Candidate Recommendation of 18 December 2014

#### I.3.1 Substantive Changes

1. If a value in a map constructor or a member in an array constructor is a map or array, it is copied. If a value in a map constructor or a member in an array constructor is a node, it is not copied. Resolves [Bug 26958](https://www.w3.org/Bugs/Public/show_bug.cgi?id=26958).
2. In the definition of numeric, we now state that all numeric types are member types of `xs:numeric`. Resolves [Bug 20631](https://www.w3.org/Bugs/Public/show_bug.cgi?id=20631).
3. Modified rule 14 of **2.5.6.2 The judgement subtype-itemtype(Ai, Bi)**. Resolves [Bug 27175](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27175).
4. In **3.11.3.1 Unary Lookup**, if the context item is not a map or an array, a type error [err:XPTY0004] is raised. If the array index is out of bounds, [err:FOAY0001] is raised. Resolves [Bug 27382](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27382).
5. Changed the semantics of **3.11.3.2 Postfix Lookup** to `for $a in E, $b in S return $a($b)`. Resolves [Bug 27536](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27536).
6. Arrays in element content are flattened, not atomized. Resolves [Bug 27463](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27463).
7. **3.16 Arrow operator (=>)** is now well defined when the left hand operand is a sequence rather than an item. Partially resolves [Bug 27537](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27537).

#### I.3.2 Editorial Changes

1. Modified the wording used to describe node identity per [Bug 27048](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27048), comment #2.
2. Fixed specification gaps in unary lookup. Resolves [Bug 27455](https://www.w3.org/Bugs/Public/show_bug.cgi?id=27455).

### I.4 Changes introduced in prior Working Drafts

1. Added **3.11.1 Maps** and **3.11.2 Arrays**. These are the most important new features in XPath 3.1
2. Clarified error code XQST0134 for XPath implementations that do not support the namespace axis, default axis for namespace-node() in abbreviated syntax. Resolves [Bug 26788](https://www.w3.org/Bugs/Public/show_bug.cgi?id=26788).
3. Simplified type conversions for value comparisons and orderspecs, eliminating the concept of lowest common supertype. Resolves [Bug 26453](https://www.w3.org/Bugs/Public/show_bug.cgi?id=26453).
4. Modified text of **3.7.2 General Comparisons** to clarify that the result of a comparison can be either false or an error. Resolves [Bug 26832](https://www.w3.org/Bugs/Public/show_bug.cgi?id=26832).
5. Added **3.11.1.1 Map Constructors** and **3.11.1.2 Map Lookup using Function Call Syntax**.
6. Added **3.11.2.1 Array Constructors** and **3.11.2.2 Array Lookup using Function Call Syntax**.
7. Defined **2.4.2 Atomization** of an array (atomization of a map is an error).
8. Added **2.5.5.8 Map Test** and **2.5.5.9 Array Test** to test whether an item is a map or an array respectively.
9. Added `exponent-separator` to the static context to support `fn:format-number()`.
10. Eliminated use of to array functions that are no longer in Functions & and Operators, such as `fn:seq()`. Changed `ay:` prefix to `array:` to match current Functions & and Operators.
11. Added **3.11.1.2 Map Lookup using Function Call Syntax**, replacing the less general map lookup operator from the previous Working Draft.
12. **3.11.2.2 Array Lookup using Function Call Syntax** with negative integer arguments are no longer type errors, they are dynamic errors.
13. If the keys in a **3.11.1.1 Map Constructors** contain both date/time values with a timezone and date/time values with no timezone, a dynamic error is raised.
14. In maps, keys of type `xs:untypedAtomic` are no longer converted to `xs:string`.

↑