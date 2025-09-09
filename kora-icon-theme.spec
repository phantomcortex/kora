Name:           kora-icon-theme
Version:        __VERSION__
Release:        %autorelease
Summary:        Forked Icon theme with Steam Game art and others

License:        GPL-3.0
URL:            https://github.com/phantomcortex/kora 
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  findutils
Requires:       shared-mime-info
Requires:       gtk-update-icon-cache

%description
Kora is a beautifully designed icon theme featuring custom Steam game icons
and various application icons. This theme provides a modern, consistent look
across your desktop environment with support for multiple icon sizes and
both light and dark variants.

%prep
%autosetup -n %{name}-%{version}

%build
# No build required for icon themes

%install
rm -rf %{buildroot}

# Create necessary directories
mkdir -p %{buildroot}%{_datadir}/icons
mkdir -p %{buildroot}%{_datadir}/mime/packages

# Install MIME types if present
if [ -d "mime/packages" ]; then
    echo "Installing MIME type definitions..."
    cp -r mime/packages/* %{buildroot}%{_datadir}/mime/packages/
    
    # Set proper permissions for MIME files
    find %{buildroot}%{_datadir}/mime/packages -type f -exec chmod 644 {} \;
fi

# Install all kora icon theme variants
for theme_dir in kora kora-light kora-light-panel kora-pgrey; do
    if [ -d "$theme_dir" ]; then
        echo "Installing icon theme: $theme_dir"
        cp -r "$theme_dir" %{buildroot}%{_datadir}/icons/
        
        # Ensure proper permissions
        find %{buildroot}%{_datadir}/icons/"$theme_dir" -type f -exec chmod 644 {} \;
        find %{buildroot}%{_datadir}/icons/"$theme_dir" -type d -exec chmod 755 {} \;
        
        # Verify index.theme exists
        if [ ! -f %{buildroot}%{_datadir}/icons/"$theme_dir"/index.theme ]; then
            echo "Warning: index.theme missing in $theme_dir"
            # Create a basic index.theme if missing
            cat > %{buildroot}%{_datadir}/icons/"$theme_dir"/index.theme <<EOF
[Icon Theme]
Name=$theme_dir
Comment=Kora icon theme variant
Inherits=hicolor
Directories=scalable/apps,scalable/mimetypes,scalable/places
EOF
        fi
    fi
done

%check
# Basic validation
for theme_dir in %{buildroot}%{_datadir}/icons/kora*; do
    if [ -d "$theme_dir" ]; then
        if [ ! -f "$theme_dir/index.theme" ]; then
            echo "ERROR: Missing index.theme in $theme_dir"
            exit 1
        fi
    fi
done

%files
%license LICENSE* COPYING*
%doc README* AUTHORS* CHANGELOG*
%{_datadir}/icons/kora*/
%{_datadir}/mime/packages/*

%post
# Update icon cache for all installed themes
for theme_dir in %{_datadir}/icons/kora*; do
    if [ -d "$theme_dir" ]; then
        /bin/touch --no-create "$theme_dir" &>/dev/null || :
        if [ -x %{_bindir}/gtk-update-icon-cache ]; then
            %{_bindir}/gtk-update-icon-cache --quiet "$theme_dir" &>/dev/null || :
        fi
    fi
done

# Update MIME database
if [ -x %{_bindir}/update-mime-database ]; then
    %{_bindir}/update-mime-database %{_datadir}/mime &>/dev/null || :
fi

%postun
# Update icon cache after removal
if [ $1 -eq 0 ]; then
    for theme_dir in %{_datadir}/icons/kora*; do
        if [ -d "$theme_dir" ]; then
            /bin/touch --no-create "$theme_dir" &>/dev/null || :
            if [ -x %{_bindir}/gtk-update-icon-cache ]; then
                %{_bindir}/gtk-update-icon-cache --quiet "$theme_dir" &>/dev/null || :
            fi
        fi
    done
    
    # Update MIME database after removal
    if [ -x %{_bindir}/update-mime-database ]; then
        %{_bindir}/update-mime-database %{_datadir}/mime &>/dev/null || :
    fi
fi

%changelog
%autochangelog
