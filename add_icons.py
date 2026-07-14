import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if '@phosphor-icons' not in content:
    content = content.replace('</head>', '  <script src="https://unpkg.com/@phosphor-icons/web"></script>\n</head>')

replacements = {
    'data-icon="🛠️">Dashboard</a>': '><i class="ph ph-chart-bar" style="margin-right: 5px; font-size: 1.2em; vertical-align: middle;"></i>Dashboard</a>',
    'data-icon="🔐">Login</a>': '><i class="ph ph-lock-key" style="margin-right: 5px; font-size: 1.2em; vertical-align: middle;"></i>Login</a>',
    '>Overview</a>': '><i class="ph ph-house" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Overview</a>',
    '>Login Portals</a>': '><i class="ph ph-sign-in" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Login Portals</a>',
    '>Sponsors</a>': '><i class="ph ph-handshake" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Sponsors</a>',
    '>Clients</a>': '><i class="ph ph-users" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Clients</a>',
    '>Marketing</a>': '><i class="ph ph-megaphone" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Marketing</a>',
    '>Register</a>': '><i class="ph ph-user-plus" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Register</a>',
    '>About</a>': '><i class="ph ph-info" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>About</a>',
    '>Media</a>': '><i class="ph ph-image" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Media</a>',
    '>Team</a>': '><i class="ph ph-users-three" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Team</a>',
    '>Live Registration</a>': '><i class="ph ph-activity" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Live Registration</a>',
    '>Contact</a>': '><i class="ph ph-envelope-simple" style="margin-right: 5px; font-size: 1.1em; vertical-align: middle;"></i>Contact</a>',
    '<button type="submit">Register as Sponsor</button>': '<button type="submit"><i class="ph ph-paper-plane-right" style="margin-right: 5px; font-size: 1.2em; vertical-align: middle;"></i>Register as Sponsor</button>',
    '<button type="submit">Register as Client</button>': '<button type="submit"><i class="ph ph-paper-plane-right" style="margin-right: 5px; font-size: 1.2em; vertical-align: middle;"></i>Register as Client</button>',
    'data-icon="🔑">Login</button>': '><i class="ph ph-key" style="margin-right: 5px; font-size: 1.2em; vertical-align: middle;"></i>Login</button>',
    'data-icon="❌">Cancel</button>': '><i class="ph ph-x" style="margin-right: 5px; font-size: 1.2em; vertical-align: middle;"></i>Cancel</button>'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
