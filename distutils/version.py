"""
Version module compatibility for distutils
"""

class LooseVersion:
    """
    A simple version comparison class that mimics distutils.version.LooseVersion
    """
    def __init__(self, vstring=None):
        self.vstring = str(vstring) if vstring is not None else ""
        self.version = self._parse_version(self.vstring)
    
    def _parse_version(self, vstring):
        """Parse version string into comparable components"""
        import re
        # Split on dots, hyphens, and other separators
        parts = re.split(r'[.\-_]', vstring.lower())
        version = []
        for part in parts:
            # Try to convert to int, otherwise keep as string
            try:
                version.append(int(part))
            except ValueError:
                # Handle alpha, beta, rc versions
                if part in ('alpha', 'a'):
                    version.append(-3)
                elif part in ('beta', 'b'):
                    version.append(-2)
                elif part in ('rc', 'c'):
                    version.append(-1)
                else:
                    version.append(part)
        return version
    
    def __str__(self):
        return self.vstring
    
    def __repr__(self):
        return f"LooseVersion('{self.vstring}')"
    
    def __eq__(self, other):
        return self._cmp(other) == 0
    
    def __lt__(self, other):
        return self._cmp(other) < 0
    
    def __le__(self, other):
        return self._cmp(other) <= 0
    
    def __gt__(self, other):
        return self._cmp(other) > 0
    
    def __ge__(self, other):
        return self._cmp(other) >= 0
    
    def __ne__(self, other):
        return self._cmp(other) != 0
    
    def _cmp(self, other):
        if isinstance(other, str):
            other = LooseVersion(other)
        elif not isinstance(other, LooseVersion):
            return NotImplemented
        
        # Compare version components
        a, b = self.version, other.version
        
        # Pad the shorter version with zeros
        max_len = max(len(a), len(b))
        a = a + [0] * (max_len - len(a))
        b = b + [0] * (max_len - len(b))
        
        for i in range(max_len):
            if a[i] < b[i]:
                return -1
            elif a[i] > b[i]:
                return 1
        return 0