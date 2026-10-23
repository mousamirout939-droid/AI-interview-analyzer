"""Original programming-language learning notes and examples for the site."""

LEARNING_LANGUAGES = [
    {
        "slug": "python",
        "name": "Python",
        "category": "General purpose",
        "summary": "A readable, high-level language used for automation, web services, data, and AI.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Start with values, variables, output, and indentation-based blocks.",
                "topics": [{
                    "title": "Variables, types, and conditions",
                    "notes": [
                        "Names are case-sensitive and do not need a declaration keyword.",
                        "Indentation defines a block; use four spaces consistently.",
                    ],
                    "code": 'name = "Ada"\nage = 28\n\nif age >= 18:\n    print(f"{name} is an adult")',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Organize logic into reusable functions and work with collections.",
                "topics": [{
                    "title": "Functions and comprehensions",
                    "notes": [
                        "A function returns a value with return; type hints document expected inputs and outputs.",
                        "A comprehension creates a new collection without mutating the source.",
                    ],
                    "code": 'def even_squares(values: list[int]) -> list[int]:\n    return [value ** 2 for value in values if value % 2 == 0]\n\nprint(even_squares([1, 2, 3, 4]))',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Use generators to process large or streaming data without building it all in memory.",
                "topics": [{
                    "title": "Generators and lazy iteration",
                    "notes": [
                        "yield pauses a function and resumes it on the next iteration.",
                        "A generator can represent an unbounded sequence while keeping memory use small.",
                    ],
                    "code": 'def batches(items, size):\n    for start in range(0, len(items), size):\n        yield items[start:start + size]\n\nfor batch in batches([1, 2, 3, 4, 5], 2):\n    print(batch)',
                }],
            },
        ],
    },
    {
        "slug": "javascript",
        "name": "JavaScript",
        "category": "Web development",
        "summary": "The language of the browser, also used for servers, tools, and cross-platform apps.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Learn values, block-scoped variables, and decisions.",
                "topics": [{
                    "title": "Variables and conditions",
                    "notes": [
                        "Prefer const by default and use let when a binding must be reassigned.",
                        "=== compares values without implicit type conversion.",
                    ],
                    "code": 'const score = 82;\nlet result = "keep practising";\n\nif (score >= 70) {\n  result = "ready for the next step";\n}\nconsole.log(result);',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Use functions, arrays, and object transformations to model everyday tasks.",
                "topics": [{
                    "title": "Array methods and functions",
                    "notes": [
                        "map transforms each item; filter keeps matching items.",
                        "Arrow functions are concise function expressions and preserve lexical this.",
                    ],
                    "code": 'const prices = [12, 25, 8, 30];\nconst discounted = prices\n  .filter(price => price >= 10)\n  .map(price => price * 0.9);\n\nconsole.log(discounted);',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Handle asynchronous work with promises and async functions.",
                "topics": [{
                    "title": "Async and await",
                    "notes": [
                        "An async function always returns a Promise.",
                        "Await pauses that function until a Promise settles; use try/catch for failures.",
                    ],
                    "code": 'async function loadUser(id) {\n  const response = await fetch(`/api/users/${id}`);\n  if (!response.ok) throw new Error("Could not load user");\n  return response.json();\n}\n\nloadUser(7).then(console.log).catch(console.error);',
                }],
            },
        ],
    },
    {
        "slug": "html-css",
        "name": "HTML & CSS",
        "category": "Web development",
        "summary": "HTML gives a page structure; CSS controls its visual presentation and responsive layout.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Build semantic content and style it with selectors and declarations.",
                "topics": [{
                    "title": "A semantic page and a CSS rule",
                    "notes": [
                        "Choose elements for their meaning, such as main, article, and button.",
                        "A CSS rule combines a selector with one or more property-value declarations.",
                    ],
                    "code": '<main class="card">\n  <h1>My first page</h1>\n  <p>Clear structure helps everyone.</p>\n</main>\n\n<style>\n  .card { padding: 1rem; border-radius: 12px; }\n</style>',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Create flexible layouts that adapt naturally to different screen sizes.",
                "topics": [{
                    "title": "Responsive grid",
                    "notes": [
                        "CSS Grid is useful for two-dimensional layouts.",
                        "minmax() and auto-fit allow columns to wrap without a fixed breakpoint.",
                    ],
                    "code": '<section class="cards">\n  <article>One</article>\n  <article>Two</article>\n  <article>Three</article>\n</section>\n\n<style>\n  .cards {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));\n    gap: 1rem;\n  }\n</style>',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Use custom properties and accessible focus states to build maintainable interfaces.",
                "topics": [{
                    "title": "Design tokens and focus visibility",
                    "notes": [
                        "Custom properties centralize values and can be overridden by themes.",
                        "Keep keyboard focus visible; do not remove outlines without a clear replacement.",
                    ],
                    "code": ':root { --space: 1rem; --brand: #6847a5; }\n\n.button {\n  padding: var(--space) calc(var(--space) * 1.5);\n  background: var(--brand);\n  color: white;\n}\n\n.button:focus-visible {\n  outline: 3px solid currentColor;\n  outline-offset: 3px;\n}',
                }],
            },
        ],
    },
    {
        "slug": "java",
        "name": "Java",
        "category": "General purpose",
        "summary": "A statically typed, object-oriented language widely used for backend and Android systems.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Declare typed values and make decisions with explicit conditions.",
                "topics": [{
                    "title": "Types and conditionals",
                    "notes": [
                        "Java variables have declared types, checked by the compiler.",
                        "The main method is a common application entry point.",
                    ],
                    "code": 'class Main {\n    public static void main(String[] args) {\n        int score = 82;\n        if (score >= 70) {\n            System.out.println("Pass");\n        }\n    }\n}',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Represent related data with classes and protect invariants through methods.",
                "topics": [{
                    "title": "Classes and constructors",
                    "notes": [
                        "A constructor initializes an instance when it is created.",
                        "Keep fields private and expose behavior through methods where appropriate.",
                    ],
                    "code": 'class Counter {\n    private int value;\n\n    public Counter(int initialValue) {\n        value = initialValue;\n    }\n\n    public int increment() {\n        return ++value;\n    }\n}',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Use generic types to write reusable code while retaining compile-time checks.",
                "topics": [{
                    "title": "Generic methods",
                    "notes": [
                        "A type parameter lets a method work with multiple reference types.",
                        "The compiler verifies that the returned value matches the input type.",
                    ],
                    "code": 'import java.util.List;\n\nclass Main {\n    static <T> T first(List<T> items) {\n        if (items.isEmpty()) throw new IllegalArgumentException("empty list");\n        return items.get(0);\n    }\n}',
                }],
            },
        ],
    },
    {
        "slug": "c",
        "name": "C",
        "category": "Systems programming",
        "summary": "A compact compiled language that gives direct control over memory and hardware interfaces.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Write a program entry point, declare values, and print formatted output.",
                "topics": [{
                    "title": "Variables and output",
                    "notes": [
                        "C requires declarations with types such as int and double.",
                        "The format specifier in printf must match the value type.",
                    ],
                    "code": '#include <stdio.h>\n\nint main(void) {\n    int count = 3;\n    printf("Count: %d\\n", count);\n    return 0;\n}',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Use functions and arrays to break a program into reusable operations.",
                "topics": [{
                    "title": "Functions and arrays",
                    "notes": [
                        "An array stores same-typed elements in contiguous memory.",
                        "Pass the element count to a function because array parameters do not carry their length.",
                    ],
                    "code": '#include <stddef.h>\n\nint sum(const int values[], size_t length) {\n    int total = 0;\n    for (size_t i = 0; i < length; i++) {\n        total += values[i];\n    }\n    return total;\n}',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Pointers refer to memory locations; use them carefully and document ownership.",
                "topics": [{
                    "title": "Dynamic memory",
                    "notes": [
                        "Check allocation results before using returned memory.",
                        "Every successful malloc must eventually be paired with free by the owner.",
                    ],
                    "code": '#include <stdlib.h>\n\nint *make_value(int value) {\n    int *result = malloc(sizeof *result);\n    if (result == NULL) return NULL;\n    *result = value;\n    return result;\n}\n\n/* Caller uses the value, then calls free(pointer). */',
                }],
            },
        ],
    },
    {
        "slug": "cpp",
        "name": "C++",
        "category": "Systems programming",
        "summary": "A compiled language combining low-level control with abstractions for modern applications.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Use types, standard library output, and a conventional main function.",
                "topics": [{
                    "title": "Output and variables",
                    "notes": [
                        "C++ adds standard library facilities such as std::cout.",
                        "Prefer clear initialization and avoid uninitialized local variables.",
                    ],
                    "code": '#include <iostream>\n#include <string>\n\nint main() {\n    std::string name = "Ada";\n    std::cout << "Hello, " << name << "!\\n";\n}',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Use standard containers and range-based loops to manage collections.",
                "topics": [{
                    "title": "Vectors and range loops",
                    "notes": [
                        "std::vector manages a dynamically sized sequence.",
                        "Use const references when reading larger values without copying.",
                    ],
                    "code": '#include <iostream>\n#include <vector>\n\nint main() {\n    const std::vector<int> scores{72, 91, 84};\n    for (const int score : scores) {\n        std::cout << score << "\\n";\n    }\n}',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Express ownership with smart pointers rather than manually managed object lifetimes.",
                "topics": [{
                    "title": "Unique ownership",
                    "notes": [
                        "std::unique_ptr owns one object and releases it automatically.",
                        "Move ownership explicitly; use shared ownership only when it is genuinely shared.",
                    ],
                    "code": '#include <memory>\n\nstruct Session {\n    int id;\n};\n\nint main() {\n    auto session = std::make_unique<Session>();\n    session->id = 42;\n}',
                }],
            },
        ],
    },
    {
        "slug": "csharp",
        "name": "C#",
        "category": "General purpose",
        "summary": "A strongly typed .NET language used for web services, desktop apps, games, and cloud software.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Use typed variables, interpolation, and branching in a simple program.",
                "topics": [{
                    "title": "Values and interpolation",
                    "notes": [
                        "var asks the compiler to infer a local variable's static type.",
                        "String interpolation inserts expressions inside a dollar-prefixed string.",
                    ],
                    "code": 'var name = "Ada";\nvar score = 82;\n\nif (score >= 70)\n{\n    Console.WriteLine($"{name} passed");\n}',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Use records to model immutable data and LINQ to query collections.",
                "topics": [{
                    "title": "Records and LINQ",
                    "notes": [
                        "A record is useful for data-centric types with value-based equality.",
                        "LINQ filters and projects sequences while keeping the intent readable.",
                    ],
                    "code": 'using System.Linq;\n\nrecord Candidate(string Name, int Score);\n\nclass Program {\n    static void Main() {\n        var candidates = new[] {\n            new Candidate("Ari", 91),\n            new Candidate("Sam", 68)\n        };\n        var strong = candidates.Where(candidate => candidate.Score >= 80);\n    }\n}',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Compose asynchronous operations without blocking the calling thread.",
                "topics": [{
                    "title": "Async methods",
                    "notes": [
                        "Task<T> represents work that may complete in the future.",
                        "Await asynchronous I/O instead of blocking a thread with .Result or .Wait().",
                    ],
                    "code": 'using System.Net.Http;\nusing System.Threading.Tasks;\n\nclass Example {\n    static async Task<string> ReadAsync(HttpClient client, string url)\n    {\n        using var response = await client.GetAsync(url);\n        response.EnsureSuccessStatusCode();\n        return await response.Content.ReadAsStringAsync();\n    }\n}',
                }],
            },
        ],
    },
    {
        "slug": "rust",
        "name": "Rust",
        "category": "Systems programming",
        "summary": "A compiled systems language focused on performance and memory safety without a garbage collector.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Start with immutable bindings, explicit mutability, and pattern-based branching.",
                "topics": [{
                    "title": "Bindings and conditions",
                    "notes": [
                        "Bindings are immutable by default; add mut only when reassignment is needed.",
                        "Rust uses expression-oriented syntax, so blocks can produce values.",
                    ],
                    "code": 'fn main() {\n    let mut score = 60;\n    score += 25;\n\n    if score >= 70 {\n        println!("Pass: {score}");\n    }\n}',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Use enums and pattern matching to represent alternatives explicitly.",
                "topics": [{
                    "title": "Enums and match",
                    "notes": [
                        "An enum can carry different data in each variant.",
                        "match must handle every possible variant unless a wildcard arm is used.",
                    ],
                    "code": 'enum Status {\n    Ready,\n    Failed(String),\n}\n\nfn describe(status: Status) -> String {\n    match status {\n        Status::Ready => "ready".to_string(),\n        Status::Failed(reason) => format!("failed: {reason}"),\n    }\n}',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Model fallible operations with Result and propagate errors with the question-mark operator.",
                "topics": [{
                    "title": "Result-based error handling",
                    "notes": [
                        "Result<T, E> represents either success or an error value.",
                        "The ? operator returns an error to the caller, keeping error flow explicit.",
                    ],
                    "code": 'use std::fs;\nuse std::io;\n\nfn load_config(path: &str) -> Result<String, io::Error> {\n    let contents = fs::read_to_string(path)?;\n    Ok(contents)\n}',
                }],
            },
        ],
    },
    {
        "slug": "php",
        "name": "PHP",
        "category": "Web development",
        "summary": "A server-side scripting language commonly used to build dynamic websites and APIs.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Declare variables with a dollar sign and use clear control flow.",
                "topics": [{
                    "title": "Variables and output",
                    "notes": [
                        "PHP variables begin with $ and are dynamically typed.",
                        "Use strict comparisons when type conversion is not intended.",
                    ],
                    "code": '<?php\n$name = "Ada";\n$score = 82;\n\nif ($score >= 70) {\n    echo "Hello, " . $name;\n}',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Use typed functions and associative arrays to structure application data.",
                "topics": [{
                    "title": "Functions and arrays",
                    "notes": [
                        "Parameter and return types make function contracts easier to understand.",
                        "Associative arrays map readable string keys to values.",
                    ],
                    "code": '<?php\ndeclare(strict_types=1);\n\nfunction greeting(string $name): string {\n    return "Hello, " . $name;\n}\n\n$user = ["name" => "Ada", "active" => true];\necho greeting($user["name"]);',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Use prepared statements so database values are treated as data, not SQL syntax.",
                "topics": [{
                    "title": "Parameterized database queries",
                    "notes": [
                        "Bind untrusted values as parameters instead of concatenating them into SQL.",
                        "Handle database errors explicitly and keep credentials outside source code.",
                    ],
                    "code": '<?php\n$stmt = $pdo->prepare(\n    "SELECT id, name FROM users WHERE email = :email"\n);\n$stmt->execute(["email" => $email]);\n$user = $stmt->fetch(PDO::FETCH_ASSOC);',
                }],
            },
        ],
    },
    {
        "slug": "sql",
        "name": "SQL",
        "category": "Data",
        "summary": "A declarative language for defining, querying, and changing relational data.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Select only the columns and rows needed from a table.",
                "topics": [{
                    "title": "Filtering and sorting",
                    "notes": [
                        "WHERE filters rows before the result is returned.",
                        "ORDER BY makes result ordering explicit; without it, row order is not guaranteed.",
                    ],
                    "code": 'SELECT name, score\nFROM candidates\nWHERE score >= 70\nORDER BY score DESC;',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Combine related tables and summarize rows with grouping.",
                "topics": [{
                    "title": "Joins and aggregation",
                    "notes": [
                        "A join combines rows using a relationship between tables.",
                        "GROUP BY creates groups; aggregate functions calculate a value for each group.",
                    ],
                    "code": 'SELECT teams.name, COUNT(candidates.id) AS candidate_count\nFROM teams\nLEFT JOIN candidates ON candidates.team_id = teams.id\nGROUP BY teams.id, teams.name;',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Use a common table expression to name a query step and build on its result.",
                "topics": [{
                    "title": "Common table expressions",
                    "notes": [
                        "A CTE improves readability by separating a complex query into named steps.",
                        "Window functions compute across related rows without collapsing them like GROUP BY.",
                    ],
                    "code": 'WITH ranked AS (\n  SELECT name, team_id, score,\n         ROW_NUMBER() OVER (\n           PARTITION BY team_id ORDER BY score DESC\n         ) AS position\n  FROM candidates\n)\nSELECT name, team_id, score\nFROM ranked\nWHERE position = 1;',
                }],
            },
        ],
    },
    {
        "slug": "typescript",
        "name": "TypeScript",
        "category": "Web development",
        "summary": "JavaScript with a static type system that catches many mistakes before code runs.",
        "levels": [
            {
                "id": "basics",
                "label": "Basics",
                "intro": "Annotate values and function parameters to make expected data explicit.",
                "topics": [{
                    "title": "Types and functions",
                    "notes": [
                        "TypeScript checks types during development and emits JavaScript for execution.",
                        "Type annotations do not change JavaScript runtime behavior.",
                    ],
                    "code": 'function greet(name: string): string {\n  return `Hello, ${name}`;\n}\n\nconst message = greet("Ada");',
                }],
            },
            {
                "id": "intermediate",
                "label": "Intermediate",
                "intro": "Describe structured objects and narrow union types before using them.",
                "topics": [{
                    "title": "Interfaces and narrowing",
                    "notes": [
                        "An interface describes the shape an object should have.",
                        "A discriminant property lets TypeScript safely narrow a union.",
                    ],
                    "code": 'type Result =\n  | { kind: "success"; value: number }\n  | { kind: "error"; message: string };\n\nfunction display(result: Result): string {\n  if (result.kind === "success") return String(result.value);\n  return result.message;\n}',
                }],
            },
            {
                "id": "advanced",
                "label": "Advanced",
                "intro": "Use generics to preserve relationships between inputs and outputs.",
                "topics": [{
                    "title": "Generic constraints",
                    "notes": [
                        "A generic keeps type information instead of reducing values to any.",
                        "A constraint limits the allowed type while retaining its specific properties.",
                    ],
                    "code": 'function getLength<T extends { length: number }>(value: T): number {\n  return value.length;\n}\n\ngetLength("hello");\ngetLength([1, 2, 3]);',
                }],
            },
        ],
    },
]
