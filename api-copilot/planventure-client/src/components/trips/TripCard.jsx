import { 
  Card, 
  CardContent, 
  CardMedia, 
  Typography, 
  CardActions, 
  Button,
  Chip,
  Box,
  Skeleton
} from '@mui/material';
import { 
  LocationOn, 
  DateRange,
  ArrowForward 
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const TripCard = ({ trip, loading }) => {
  const navigate = useNavigate();

  if (loading) {
    return (
      <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Skeleton variant="rectangular" height={140} />
        <CardContent>
          <Skeleton variant="text" height={32} width="80%" />
          <Skeleton variant="text" height={24} width="60%" />
          <Skeleton variant="text" height={24} width="40%" />
        </CardContent>
        <CardActions>
          <Skeleton variant="rectangular" width={100} height={36} />
        </CardActions>
      </Card>
    );
  }
  return (
    <Card 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 3,
        },
      }}
    >
      <CardContent sx={{ flexGrow: 1, p: 3 }}>
        <Typography gutterBottom variant="h5" component="h2" sx={{ fontWeight: 600 }}>
          {trip.title}
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <LocationOn fontSize="small" color="primary" />
          <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
            {trip.destination}
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <DateRange fontSize="small" color="primary" />
          <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
            {new Date(trip.start_date).toLocaleDateString()} - {new Date(trip.end_date).toLocaleDateString()}
          </Typography>
        </Box>
        {trip.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {trip.description.length > 100 
              ? `${trip.description.substring(0, 100)}...` 
              : trip.description
            }
          </Typography>
        )}
        <Chip 
          label={trip.status || 'Planning'} 
          size="small" 
          color="primary" 
          variant="outlined"
        />
      </CardContent>
      <CardActions sx={{ p: 2, pt: 0 }}>
        <Button 
          size="small" 
          endIcon={<ArrowForward />}
          onClick={() => navigate(`/trips/${trip.id}`)}
          fullWidth
          variant="outlined"
        >
          View Details
        </Button>
      </CardActions>
    </Card>
  );
};

export default TripCard;
