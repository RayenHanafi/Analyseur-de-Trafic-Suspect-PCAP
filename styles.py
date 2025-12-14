#!/usr/bin/env python3
"""
Module contenant les styles CSS pour le rapport HTML
"""

def get_css_styles():
    """Retourne le code CSS complet pour le rapport"""
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --bg-1: #071028; /* darkest */
            --bg-2: #0b2a4a;
            --accent-1: #1ea7ff;
            --accent-2: #3b82f6;
            --glass: rgba(255,255,255,0.03);
            --muted: rgba(230,245,255,0.85);
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: radial-gradient(1200px 600px at 10% 10%, rgba(14,37,78,0.6), transparent 10%),
                        radial-gradient(1000px 400px at 90% 90%, rgba(6,20,48,0.6), transparent 10%),
                        linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
            padding: 28px;
            color: var(--muted);
            -webkit-font-smoothing:antialiased;
            -moz-osx-font-smoothing:grayscale;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            border-radius: 14px;
            box-shadow: 0 10px 30px rgba(3,10,25,0.6), 0 0 40px rgba(30,167,255,0.03) inset;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.04);
            backdrop-filter: blur(6px);
        }

        .header {
            background: linear-gradient(90deg, rgba(30,167,255,0.12), rgba(59,130,246,0.08));
            color: var(--muted);
            padding: 44px 36px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }

        .header h1 {
            font-size: 2.4em;
            margin-bottom: 6px;
            color: #eaf6ff;
            letter-spacing: -0.5px;
            text-shadow: 0 6px 18px rgba(14,37,78,0.6);
        }

        .header p {
            font-size: 1em;
            opacity: 0.9;
            color: #bfe8ff;
        }

        .content { padding: 36px; }

        .section {
            margin-bottom: 30px;
            padding: 22px;
            background: var(--glass);
            border-radius: 10px;
            border-left: 4px solid rgba(30,167,255,0.16);
            box-shadow: 0 6px 18px rgba(3,10,25,0.45);
            animation: fadeIn 0.6s ease-out;
        }

        .section h2 {
            color: #cfefff;
            margin-bottom: 14px;
            font-size: 1.6em;
            display: flex;
            align-items: center;
        }

        .section h2::before {
            content: '◉';
            margin-right: 10px;
            color: var(--accent-1);
            font-size: 0.9em;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
            background: transparent;
            border-radius: 8px;
            overflow: hidden;
        }

        th {
            background: linear-gradient(90deg, rgba(30,167,255,0.08), rgba(59,130,246,0.06));
            color: #dff6ff;
            padding: 14px 16px;
            text-align: left;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.6px;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }

        td {
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.02);
            color: #c9e8ff;
        }

        tr:last-child td { border-bottom: none; }

        tr:hover {
            background: linear-gradient(90deg, rgba(30,167,255,0.02), rgba(59,130,246,0.02));
            transition: background 0.25s ease;
        }

        .badge {
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 0.8em;
            font-weight: 700;
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: white;
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
            box-shadow: 0 6px 18px rgba(30,167,255,0.12);
        }

        .critique { background: linear-gradient(90deg,#ff6b6b,#ff4959); }
        .haute { background: linear-gradient(90deg,#ff8a4c,#ff6b2a); }
        .moyenne { background: linear-gradient(90deg,#ffd86b,#ffb84d); color: #0b2033; }
        .basse { background: linear-gradient(90deg,#49d48b,#21b573); }

        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
            margin-top: 18px;
        }

        .stat-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            padding: 22px;
            border-radius: 10px;
            box-shadow: 0 8px 30px rgba(3,10,25,0.5);
            text-align: center;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            border: 1px solid rgba(255,255,255,0.03);
        }

        .stat-card:hover { transform: translateY(-6px); box-shadow: 0 18px 50px rgba(3,10,25,0.6); }

        .stat-card h3 {
            color: linear-gradient(90deg, var(--accent-1), var(--accent-2));
            font-size: 2.2em;
            margin-bottom: 8px;
            font-weight: 800;
            background: -webkit-linear-gradient(#e6f7ff, #9fd8ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stat-card p { color: #bfe8ff; font-size: 1em; font-weight: 600; }

        .alert {
            background: rgba(255,255,255,0.02);
            border-left: 5px solid rgba(255,200,24,0.12);
            padding: 14px;
            margin: 14px 0;
            border-radius: 6px;
            box-shadow: 0 6px 18px rgba(3,10,25,0.35);
            color: #ffeec9;
        }

        .alert strong { color: #ffd86b; }

        .footer {
            background: transparent;
            color: #9fcffb;
            padding: 18px;
            text-align: center;
            font-size: 0.9em;
            border-top: 1px solid rgba(255,255,255,0.03);
        }

        .footer p { margin: 4px 0; }

        .protocole-bar {
            height: 30px;
            background: linear-gradient(90deg, rgba(30,167,255,0.14), rgba(59,130,246,0.12));
            border-radius: 6px;
            margin: 6px 0;
            position: relative;
            transition: width 0.5s ease;
            box-shadow: 0 6px 18px rgba(3,10,25,0.5);
        }

        .protocole-bar span {
            position: absolute;
            right: 12px;
            line-height: 30px;
            color: #e6f6ff;
            font-weight: 700;
            font-size: 0.9em;
        }

        code {
            background: rgba(255,255,255,0.02);
            padding: 4px 8px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.92em;
            color: #a0e1ff;
        }

        strong { font-weight: 700; color: #e6f6ff; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }

        /* Responsive */
        @media (max-width: 768px) {
            .header h1 { font-size: 1.9em; }
            .section { padding: 14px; }
            .content { padding: 20px; }
            .stat-grid { grid-template-columns: 1fr; }
            table { font-size: 0.9em; }
            th, td { padding: 10px; }
        }

        @media print {
            body { background: white; padding: 0; color: #000; }
            .container { box-shadow: none; border: none; background: white; }
            .section { page-break-inside: avoid; background: white; color: #000; }
            .protocole-bar { print-color-adjust: exact; }
        }
"""